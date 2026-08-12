"""
Click va Payme "to'lov tasdiqlandi" degan xabarni shu serverga yuboradi.
Bu alohida jarayon sifatida ishga tushiriladi (bot.py bilan bir vaqtda):

    python webhook_server.py

Production'da bu server ochiq HTTPS manzilda turishi kerak (masalan Nginx
orqali reverse-proxy qilingan), chunki Click/Payme faqat HTTPS'ga so'rov yuboradi.

Bu yerdagi kod — ishlaydigan skelet. Click/Payme kabinetida "Callback URL"
ni shu serverning /click va /payme manzillariga ko'rsating:
    https://sizning-domain.uz/click
    https://sizning-domain.uz/payme
"""

import hashlib
import base64
import json

from aiohttp import web

import database as db
from config import (
    CLICK_SECRET_KEY,
    PAYME_MERCHANT_ID,
    PAYME_SECRET_KEY,
    PREMIUM_DAYS,
    WEBHOOK_HOST,
    WEBHOOK_PORT,
)

routes = web.RouteTableDef()


# =========================== CLICK ===========================
# Hujjat: https://docs.click.uz/  (Prepare -> Complete oqimi)

CLICK_ERROR_OK = 0
CLICK_ERROR_SIGN_FAILED = -1
CLICK_ERROR_ALREADY_PAID = -4
CLICK_ERROR_TRANSACTION_NOT_FOUND = -6


def _click_signature_valid(data: dict, secret: str) -> bool:
    action = data.get("action", "")
    sign_string = (
        f"{data.get('click_trans_id','')}{data.get('service_id','')}{secret}"
        f"{data.get('merchant_trans_id','')}{data.get('amount','')}{action}"
        f"{data.get('sign_time','')}"
    )
    if action == "1":  # Complete bosqichida merchant_prepare_id ham qatnashadi
        sign_string = (
            f"{data.get('click_trans_id','')}{data.get('service_id','')}{secret}"
            f"{data.get('merchant_trans_id','')}{data.get('merchant_prepare_id','')}"
            f"{data.get('amount','')}{action}{data.get('sign_time','')}"
        )
    expected = hashlib.md5(sign_string.encode()).hexdigest()
    return expected == data.get("sign_string", "")


@routes.post("/click")
async def click_webhook(request: web.Request):
    data = await request.post()
    data = dict(data)

    if not _click_signature_valid(data, CLICK_SECRET_KEY):
        return web.json_response({"error": CLICK_ERROR_SIGN_FAILED, "error_note": "Sign failed"})

    order_id = data.get("merchant_trans_id")
    action = data.get("action")

    if action == "0":  # Prepare
        return web.json_response({
            "click_trans_id": data.get("click_trans_id"),
            "merchant_trans_id": order_id,
            "merchant_prepare_id": order_id,
            "error": CLICK_ERROR_OK,
            "error_note": "Success",
        })

    if action == "1":  # Complete
        try:
            payment_id = int(order_id)
        except (TypeError, ValueError):
            return web.json_response({"error": CLICK_ERROR_TRANSACTION_NOT_FOUND, "error_note": "Not found"})

        await db.update_payment_status(payment_id, "paid")
        # payments jadvalida user_id ni topib premium beramiz
        # (oddiylik uchun to'g'ridan-to'g'ri so'rov)
        import aiosqlite
        from config import DB_PATH
        async with aiosqlite.connect(DB_PATH) as conn:
            cur = await conn.execute("SELECT user_id FROM payments WHERE id = ?", (payment_id,))
            row = await cur.fetchone()
        if row:
            await db.set_premium(row[0], PREMIUM_DAYS)

        return web.json_response({
            "click_trans_id": data.get("click_trans_id"),
            "merchant_trans_id": order_id,
            "merchant_confirm_id": order_id,
            "error": CLICK_ERROR_OK,
            "error_note": "Success",
        })

    return web.json_response({"error": CLICK_ERROR_OK, "error_note": "Success"})


# =========================== PAYME ===========================
# Hujjat: https://developer.help.paycom.uz/  (JSON-RPC uslubi)

def _payme_authorized(request: web.Request) -> bool:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth[6:].encode()).decode()
    except Exception:
        return False
    # Formatda: Paycom:SECRET_KEY
    return decoded.endswith(PAYME_SECRET_KEY)


@routes.post("/payme")
async def payme_webhook(request: web.Request):
    if not _payme_authorized(request):
        return web.json_response(
            {"error": {"code": -32504, "message": "Insufficient privileges"}}, status=200
        )

    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id")

    if method == "CheckPerformTransaction":
        order_id = params.get("account", {}).get("order_id")
        payment = None
        if order_id:
            import aiosqlite
            from config import DB_PATH
            async with aiosqlite.connect(DB_PATH) as conn:
                cur = await conn.execute("SELECT id FROM payments WHERE id = ?", (order_id,))
                payment = await cur.fetchone()
        if not payment:
            return web.json_response({"error": {"code": -31050, "message": "Order not found"}, "id": req_id})
        return web.json_response({"result": {"allow": True}, "id": req_id})

    if method == "CreateTransaction":
        order_id = params.get("account", {}).get("order_id")
        await db.update_payment_status(int(order_id), "pending")
        return web.json_response({
            "result": {
                "create_time": params.get("time"),
                "transaction": str(order_id),
                "state": 1,
            },
            "id": req_id,
        })

    if method == "PerformTransaction":
        order_id = params.get("id")
        # Bu yerda `order_id` aslida bizning transaction (order) ID emas,
        # to'liq ishlab chiqishda Payme transaction ID'sini alohida saqlash tavsiya etiladi.
        return web.json_response({
            "result": {"transaction": str(order_id), "perform_time": 0, "state": 2},
            "id": req_id,
        })

    if method == "CheckTransaction":
        return web.json_response({
            "result": {"state": 2, "transaction": str(params.get("id"))},
            "id": req_id,
        })

    if method == "CancelTransaction":
        return web.json_response({
            "result": {"state": -1, "transaction": str(params.get("id")), "cancel_time": 0},
            "id": req_id,
        })

    return web.json_response({"error": {"code": -32601, "message": "Method not found"}, "id": req_id})


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host=WEBHOOK_HOST, port=WEBHOOK_PORT)

"""
Click.uz bilan integratsiya.

Click ikki xil usulda ishlaydi:
1) Oddiy "to'lov havolasi" (Checkout) — foydalanuvchini shu havolaga
   yo'naltirasiz, u yerda karta ma'lumotlarini kiritadi.
2) Merchant API (Prepare/Complete) — Click serveri sizning webhook'ingizga
   so'rov yuboradi, siz uni tasdiqlaysiz. Bu qism `webhook_server.py` da.

Bu yerda (1) — tez ishga tushirish uchun eng oddiy yo'l.
Ishlashi uchun https://merchant.click.uz da ro'yxatdan o'tib,
CLICK_MERCHANT_ID, CLICK_SERVICE_ID larni .env ga yozish kerak.
"""

from urllib.parse import urlencode

from config import CLICK_MERCHANT_ID, CLICK_SERVICE_ID


def build_click_pay_url(order_id: int, amount: int, return_url: str = "") -> str:
    """
    order_id  — bizning tizimdagi noyob to'lov ID (masalan payments.id)
    amount    — so'mda summa (butun son)
    """
    params = {
        "service_id": CLICK_SERVICE_ID,
        "merchant_id": CLICK_MERCHANT_ID,
        "amount": amount,
        "transaction_param": order_id,
    }
    if return_url:
        params["return_url"] = return_url

    return f"https://my.click.uz/services/pay?{urlencode(params)}"

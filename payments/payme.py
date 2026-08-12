"""
Payme.uz bilan integratsiya.

Xuddi Click kabi, eng oddiy yo'l — Checkout havolasi orqali to'lov.
Merchant kabinetda (https://business.payme.uz) ro'yxatdan o'tib,
PAYME_MERCHANT_ID ni .env ga yozing.

Haqiqiy tasdiqlash (to'lov muvaffaqiyatli bo'lganini bilish) uchun
Payme sizning webhook'ingizga JSON-RPC so'rovlar yuboradi — bu qism
`webhook_server.py` faylida amalga oshirilgan.
"""

import base64

from config import PAYME_MERCHANT_ID


def build_payme_pay_url(order_id: int, amount_uzs: int) -> str:
    """
    amount_uzs — so'mda summa (butun son). Payme summani tiyinda kutadi
    (1 so'm = 100 tiyin), shuning uchun 100 ga ko'paytiramiz.
    """
    amount_tiyin = amount_uzs * 100
    params = f"m={PAYME_MERCHANT_ID};ac.order_id={order_id};a={amount_tiyin}"
    encoded = base64.b64encode(params.encode()).decode()
    return f"https://checkout.paycom.uz/{encoded}"

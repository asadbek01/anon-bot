import os
from dotenv import load_dotenv

load_dotenv()


def _split_ids(raw: str) -> set[int]:
    result = set()
    for part in (raw or "").split(","):
        part = part.strip()
        if part.isdigit():
            result.add(int(part))
    return result


BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
ADMIN_IDS = _split_ids(os.getenv("ADMIN_IDS", ""))

DB_PATH = os.getenv("DB_PATH", "bot.db")

# Eski yagona narx o'zgaruvchilari (webhook_server.py va boshqa joylarda
# umumiy default sifatida ishlatiladi)
PREMIUM_PRICE_STARS = int(os.getenv("PREMIUM_PRICE_STARS", "150"))
PREMIUM_PRICE_UZS = int(os.getenv("PREMIUM_PRICE_UZS", "25000"))
PREMIUM_DAYS = int(os.getenv("PREMIUM_DAYS", "30"))

# Premium uchun 4 ta muddat varianti: kalit -> (kun, Stars narxi, so'm narxi)
# "lifetime" uchun kun sifatida 100 yil (36500 kun) ishlatiladi — amalda "butunlay".
PREMIUM_PLANS = {
    "1d": {
        "days": 1,
        "stars": int(os.getenv("PREMIUM_PRICE_STARS_1D", "15")),
        "uzs": int(os.getenv("PREMIUM_PRICE_UZS_1D", "3000")),
    },
    "7d": {
        "days": 7,
        "stars": int(os.getenv("PREMIUM_PRICE_STARS_7D", "50")),
        "uzs": int(os.getenv("PREMIUM_PRICE_UZS_7D", "10000")),
    },
    "30d": {
        "days": 30,
        "stars": int(os.getenv("PREMIUM_PRICE_STARS_30D", "150")),
        "uzs": int(os.getenv("PREMIUM_PRICE_UZS_30D", "25000")),
    },
    "lifetime": {
        "days": 36500,
        "stars": int(os.getenv("PREMIUM_PRICE_STARS_LIFETIME", "500")),
        "uzs": int(os.getenv("PREMIUM_PRICE_UZS_LIFETIME", "90000")),
    },
}

CLICK_MERCHANT_ID = os.getenv("CLICK_MERCHANT_ID", "")
CLICK_SERVICE_ID = os.getenv("CLICK_SERVICE_ID", "")
CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")
CLICK_MERCHANT_USER_ID = os.getenv("CLICK_MERCHANT_USER_ID", "")

PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
PAYME_SECRET_KEY = os.getenv("PAYME_SECRET_KEY", "")
PAYME_TEST_KEY = os.getenv("PAYME_TEST_KEY", "")

WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))

DEFAULT_LANGUAGE = "uz"
SUPPORTED_LANGUAGES = ("uz", "en", "ru")

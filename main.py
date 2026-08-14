import asyncio
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
import database as db

from handlers import start, anonymous, premium, admin, ads, referral, poll

logging.basicConfig(level=logging.INFO)


# ---------- Render "Web Service" uchun health-check serveri ----------
# Render Web Service tipida deploy qilinganda, platforma PORT'ga HTTP so'rov
# yubora oladigan xizmat kutadi (aks holda "no open ports" xatosi bilan to'xtaydi).
# Bot o'zi HTTP server emas, shuning uchun shu yengil serverni alohida thread'da
# ishga tushiramiz — u faqat "Bot is running!" deb javob beradi.
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass  # Konsolni keraksiz loglar bilan to'ldirmaslik uchun


def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN .env faylida ko'rsatilmagan!")

    threading.Thread(target=run_health_server, daemon=True).start()

    await db.init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Handlerlar tartibi muhim: avval start, keyin state kutayotganlar,
    # keyin premium/admin menyu tugmalari
    dp.include_router(start.router)
    dp.include_router(anonymous.router)
    dp.include_router(premium.router)
    dp.include_router(admin.router)
    dp.include_router(ads.router)
    dp.include_router(referral.router)
    dp.include_router(poll.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

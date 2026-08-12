import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()






import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
import database as db

from handlers import start, anonymous, premium, admin, ads

logging.basicConfig(level=logging.INFO)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN .env faylida ko'rsatilmagan!")

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

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

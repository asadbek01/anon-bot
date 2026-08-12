import datetime
from typing import Optional

import aiosqlite

from config import DB_PATH, DEFAULT_LANGUAGE

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id     INTEGER PRIMARY KEY,
    username        TEXT,
    full_name       TEXT,
    language        TEXT DEFAULT 'uz',
    is_premium      INTEGER DEFAULT 0,
    premium_until   TEXT,
    created_at      TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id       INTEGER NOT NULL,
    receiver_id     INTEGER NOT NULL,
    text            TEXT NOT NULL,
    is_reply        INTEGER DEFAULT 0,
    parent_id       INTEGER,
    reaction        TEXT,
    created_at      TEXT
);

CREATE TABLE IF NOT EXISTS payments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    amount          TEXT,
    currency        TEXT,
    method          TEXT,
    status          TEXT DEFAULT 'pending',
    transaction_id  TEXT,
    created_at      TEXT
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def get_or_create_user(telegram_id: int, username: str | None, full_name: str) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cur.fetchone()
        if row:
            # Ma'lumotlarni yangilab turamiz (username o'zgargan bo'lishi mumkin)
            await db.execute(
                "UPDATE users SET username = ?, full_name = ? WHERE telegram_id = ?",
                (username, full_name, telegram_id),
            )
            await db.commit()
            return dict(row)

        now = datetime.datetime.utcnow().isoformat()
        await db.execute(
            "INSERT INTO users (telegram_id, username, full_name, language, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (telegram_id, username, full_name, DEFAULT_LANGUAGE, now),
        )
        await db.commit()
        cur = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cur.fetchone()
        return dict(row)


async def get_user(telegram_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def set_language(telegram_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE telegram_id = ?", (language, telegram_id)
        )
        await db.commit()


async def set_premium(telegram_id: int, days: int) -> str:
    until = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET is_premium = 1, premium_until = ? WHERE telegram_id = ?",
            (until, telegram_id),
        )
        await db.commit()
    return until


async def is_premium_active(telegram_id: int) -> bool:
    user = await get_user(telegram_id)
    if not user or not user["is_premium"] or not user["premium_until"]:
        return False
    until = datetime.datetime.fromisoformat(user["premium_until"])
    return until > datetime.datetime.utcnow()


async def save_message(sender_id: int, receiver_id: int, text: str,
                        is_reply: bool = False, parent_id: int | None = None) -> int:
    now = datetime.datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO messages (sender_id, receiver_id, text, is_reply, parent_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (sender_id, receiver_id, text, int(is_reply), parent_id, now),
        )
        await db.commit()
        return cur.lastrowid


async def get_message(message_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def set_reaction(message_id: int, emoji: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE messages SET reaction = ? WHERE id = ?", (emoji, message_id))
        await db.commit()


async def save_payment(user_id: int, amount: str, currency: str, method: str,
                        status: str = "pending", transaction_id: str | None = None) -> int:
    now = datetime.datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO payments (user_id, amount, currency, method, status, transaction_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, amount, currency, method, status, transaction_id, now),
        )
        await db.commit()
        return cur.lastrowid


async def update_payment_status(payment_id: int, status: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE payments SET status = ? WHERE id = ?", (status, payment_id))
        await db.commit()


# ---------- Statistika ----------

async def get_user_stats(telegram_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT COUNT(*) FROM messages WHERE receiver_id = ? AND is_reply = 0",
            (telegram_id,),
        )
        received = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM messages WHERE sender_id = ? AND is_reply = 1",
            (telegram_id,),
        )
        answered = (await cur.fetchone())[0]
        return {"received": received, "answered": answered}


async def get_global_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        users = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM users WHERE is_premium = 1")
        premium = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM messages")
        messages = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM payments WHERE status = 'paid'")
        payments = (await cur.fetchone())[0]

        return {"users": users, "premium": premium, "messages": messages, "payments": payments}


async def get_recent_messages(limit: int = 20, offset: int = 0) -> list[dict]:
    """Admin uchun: barcha yozishmalarni (haqiqiy ID lar bilan) qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM messages ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

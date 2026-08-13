import datetime
from typing import Optional

import asyncpg

from config import DATABASE_URL, DEFAULT_LANGUAGE

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id     BIGINT PRIMARY KEY,
    username        TEXT,
    full_name       TEXT,
    language        TEXT DEFAULT 'uz',
    is_premium      BOOLEAN DEFAULT FALSE,
    premium_until   TEXT,
    created_at      TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id              SERIAL PRIMARY KEY,
    sender_id       BIGINT NOT NULL,
    receiver_id     BIGINT NOT NULL,
    text            TEXT NOT NULL,
    is_reply        BOOLEAN DEFAULT FALSE,
    parent_id       INTEGER,
    reaction        TEXT,
    created_at      TEXT
);

CREATE TABLE IF NOT EXISTS payments (
    id              SERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL,
    amount          TEXT,
    currency        TEXT,
    method          TEXT,
    status          TEXT DEFAULT 'pending',
    transaction_id  TEXT,
    created_at      TEXT
);
"""

_pool: asyncpg.Pool | None = None


async def init_db() -> None:
    global _pool
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL .env (yoki Render Environment) da ko'rsatilmagan!")

    _pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=5)
    async with _pool.acquire() as conn:
        await conn.execute(SCHEMA)


def _row_to_dict(row) -> Optional[dict]:
    return dict(row) if row else None


async def get_or_create_user(telegram_id: int, username: str | None, full_name: str) -> dict:
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
        if row:
            await conn.execute(
                "UPDATE users SET username = $1, full_name = $2 WHERE telegram_id = $3",
                username, full_name, telegram_id,
            )
            row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
            return _row_to_dict(row)

        now = datetime.datetime.utcnow().isoformat()
        await conn.execute(
            "INSERT INTO users (telegram_id, username, full_name, language, created_at) "
            "VALUES ($1, $2, $3, $4, $5)",
            telegram_id, username, full_name, DEFAULT_LANGUAGE, now,
        )
        row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
        return _row_to_dict(row)


async def get_user(telegram_id: int) -> Optional[dict]:
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
        return _row_to_dict(row)


async def set_language(telegram_id: int, language: str) -> None:
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET language = $1 WHERE telegram_id = $2", language, telegram_id
        )


async def set_premium(telegram_id: int, days: int) -> str:
    until = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET is_premium = TRUE, premium_until = $1 WHERE telegram_id = $2",
            until, telegram_id,
        )
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
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO messages (sender_id, receiver_id, text, is_reply, parent_id, created_at) "
            "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
            sender_id, receiver_id, text, is_reply, parent_id, now,
        )
        return row["id"]


async def get_message(message_id: int) -> Optional[dict]:
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM messages WHERE id = $1", message_id)
        return _row_to_dict(row)


async def set_reaction(message_id: int, emoji: str) -> None:
    async with _pool.acquire() as conn:
        await conn.execute("UPDATE messages SET reaction = $1 WHERE id = $2", emoji, message_id)


async def save_payment(user_id: int, amount: str, currency: str, method: str,
                        status: str = "pending", transaction_id: str | None = None) -> int:
    now = datetime.datetime.utcnow().isoformat()
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO payments (user_id, amount, currency, method, status, transaction_id, created_at) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id",
            user_id, amount, currency, method, status, transaction_id, now,
        )
        return row["id"]


async def get_payment(payment_id: int) -> Optional[dict]:
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM payments WHERE id = $1", payment_id)
        return _row_to_dict(row)


async def update_payment_status(payment_id: int, status: str) -> None:
    async with _pool.acquire() as conn:
        await conn.execute("UPDATE payments SET status = $1 WHERE id = $2", status, payment_id)


# ---------- Statistika ----------

async def get_user_stats(telegram_id: int) -> dict:
    async with _pool.acquire() as conn:
        received = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE receiver_id = $1 AND is_reply = FALSE",
            telegram_id,
        )
        answered = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE sender_id = $1 AND is_reply = TRUE",
            telegram_id,
        )
        return {"received": received, "answered": answered}


async def get_advanced_user_stats(telegram_id: int) -> dict:
    """Faqat Premium foydalanuvchilar uchun: reaksiyalar tahlili va javob foizi."""
    async with _pool.acquire() as conn:
        total_reactions = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE receiver_id = $1 AND is_reply = FALSE "
            "AND reaction IS NOT NULL",
            telegram_id,
        )
        top_reaction_row = await conn.fetchrow(
            "SELECT reaction, COUNT(*) as cnt FROM messages "
            "WHERE receiver_id = $1 AND is_reply = FALSE AND reaction IS NOT NULL "
            "GROUP BY reaction ORDER BY cnt DESC LIMIT 1",
            telegram_id,
        )
        received = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE receiver_id = $1 AND is_reply = FALSE",
            telegram_id,
        )
        answered = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE sender_id = $1 AND is_reply = TRUE",
            telegram_id,
        )
        reply_rate = round((answered / received) * 100) if received else 0
        return {
            "total_reactions": total_reactions,
            "top_reaction": top_reaction_row["reaction"] if top_reaction_row else None,
            "reply_rate": reply_rate,
        }


async def get_global_stats() -> dict:
    async with _pool.acquire() as conn:
        users = await conn.fetchval("SELECT COUNT(*) FROM users")
        premium = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_premium = TRUE")
        messages = await conn.fetchval("SELECT COUNT(*) FROM messages")
        payments = await conn.fetchval("SELECT COUNT(*) FROM payments WHERE status = 'paid'")
        return {"users": users, "premium": premium, "messages": messages, "payments": payments}


async def get_recent_messages(limit: int = 20, offset: int = 0) -> list[dict]:
    """Admin uchun: barcha yozishmalarni (haqiqiy ID lar bilan) qaytaradi."""
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM messages ORDER BY id DESC LIMIT $1 OFFSET $2", limit, offset
        )
        return [dict(r) for r in rows]

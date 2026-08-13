from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

import database as db
from config import ADMIN_IDS
from keyboards import admin_panel_keyboard, admin_chats_nav_keyboard
from locales.texts import t

router = Router(name="admin")

PAGE_SIZE = 20


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(F.text.in_({t("main_menu_admin", "uz"), t("main_menu_admin", "en"), t("main_menu_admin", "ru")}))
async def admin_menu(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    if not _is_admin(message.from_user.id):
        await message.answer(t("admin_not_allowed", lang))
        return

    await message.answer(t("admin_panel_title", lang), reply_markup=admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]
    stats = await db.get_global_stats()

    await callback.message.answer(
        t(
            "admin_stats_text",
            lang,
            users=stats["users"],
            premium=stats["premium"],
            messages=stats["messages"],
            payments=stats["payments"],
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:chats:"))
async def admin_chats(callback: CallbackQuery, bot: Bot):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]

    offset = int(callback.data.split(":")[2])
    rows = await db.get_recent_messages(limit=PAGE_SIZE + 1, offset=offset)
    has_more = len(rows) > PAGE_SIZE
    rows = rows[:PAGE_SIZE]

    if not rows:
        await callback.message.answer(t("no_messages_yet", lang))
        await callback.answer()
        return

    lines = []
    for r in rows:
        sender = await db.get_user(r["sender_id"])
        receiver = await db.get_user(r["receiver_id"])
        sender_label = _label(sender, r["sender_id"])
        receiver_label = _label(receiver, r["receiver_id"])
        kind = "↩️" if r["is_reply"] else "📩"
        preview = (r["text"][:80] + "…") if len(r["text"]) > 80 else r["text"]
        lines.append(
            f"{kind} <b>{sender_label}</b> → <b>{receiver_label}</b>\n"
            f"<i>{r['created_at'][:16].replace('T', ' ')}</i>\n{preview}"
        )

    text = "\n\n".join(lines)
    await callback.message.answer(text, reply_markup=admin_chats_nav_keyboard(offset, has_more))
    await callback.answer()


def _label(user: dict | None, fallback_id: int) -> str:
    if not user:
        return f"ID:{fallback_id}"
    if user["username"]:
        name = f"@{user['username']}"
    else:
        name = user["full_name"] or f"ID:{fallback_id}"
    if user.get("is_premium"):
        name = f"{name} 💎"
    return name

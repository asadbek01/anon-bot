from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from locales.texts import t
from config import ADMIN_IDS


def language_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu_keyboard(lang: str, user_id: int) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=t("main_menu_link", lang)), KeyboardButton(text=t("main_menu_premium", lang))],
        [KeyboardButton(text=t("main_menu_stats", lang)), KeyboardButton(text=t("main_menu_language", lang))],
        [KeyboardButton(text=t("main_menu_ads", lang))],
    ]
    if user_id in ADMIN_IDS:
        rows.append([KeyboardButton(text=t("main_menu_admin", lang))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def message_action_keyboard(lang: str, message_id: int, receiver_is_premium: bool) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t("reply_button", lang), callback_data=f"reply:{message_id}")],
    ]
    reveal_text = t("reveal_button", lang)
    buttons.append([InlineKeyboardButton(text=reveal_text, callback_data=f"reveal:{message_id}")])
    buttons.append(_reaction_row(message_id))
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _reaction_row(message_id: int) -> list[InlineKeyboardButton]:
    emojis = ["❤️", "😂", "😮", "😢", "🔥"]
    return [
        InlineKeyboardButton(text=e, callback_data=f"react:{message_id}:{e}")
        for e in emojis
    ]


def premium_plans_keyboard(lang: str) -> InlineKeyboardMarkup:
    """4 ta muddat variantini ko'rsatadi: 1 kun / 7 kun / 1 oy / Butunlay."""
    from config import PREMIUM_PLANS

    rows = []
    for plan_key in ("1d", "7d", "30d", "lifetime"):
        plan = PREMIUM_PLANS[plan_key]
        label = t(f"plan_{plan_key}", lang, stars=plan["stars"], uzs=f"{plan['uzs']:,}".replace(",", " "))
        rows.append([InlineKeyboardButton(text=label, callback_data=f"premium_plan:{plan_key}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def payment_method_keyboard(lang: str, plan_key: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t("pay_with_stars", lang), callback_data=f"pay:stars:{plan_key}")],
        [InlineKeyboardButton(text=t("pay_with_click", lang), callback_data=f"pay:click:{plan_key}")],
        [InlineKeyboardButton(text=t("pay_with_payme", lang), callback_data=f"pay:payme:{plan_key}")],
        [InlineKeyboardButton(text=t("back", lang), callback_data="premium_back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_panel_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t("admin_all_stats", lang), callback_data="admin:stats")],
        [InlineKeyboardButton(text=t("admin_all_chats", lang), callback_data="admin:chats:0")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_chats_nav_keyboard(offset: int, has_more: bool) -> InlineKeyboardMarkup:
    row = []
    if offset > 0:
        row.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin:chats:{max(0, offset - 20)}"))
    if has_more:
        row.append(InlineKeyboardButton(text="➡️", callback_data=f"admin:chats:{offset + 20}"))
    return InlineKeyboardMarkup(inline_keyboard=[row] if row else [])

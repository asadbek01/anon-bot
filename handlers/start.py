from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database as db
from config import BOT_USERNAME, REFERRAL_BONUS_DAYS, REFERRALS_NEEDED_PER_BONUS
from keyboards import language_keyboard, main_menu_keyboard
from locales.texts import t
from states import AnonMessageStates

router = Router(name="start")


@router.message(CommandStart(deep_link=True))
async def cmd_start_with_payload(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    """
    t.me/bot?start=<owner_id>   -> anonim xabar yozish oqimi
    t.me/bot?start=ref<user_id> -> referal orqali kirish
    """
    is_new_user = (await db.get_user(message.from_user.id)) is None

    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    payload = command.args or ""

    # ---- Referal havolasi ----
    if payload.startswith("ref"):
        ref_part = payload[3:]
        if ref_part.isdigit() and is_new_user:
            referrer_id = int(ref_part)
            added = await db.add_referral(referrer_id, message.from_user.id)
            if added:
                total_referrals = await db.get_referral_count(referrer_id)
                # Faqat har REFERRALS_NEEDED_PER_BONUS ta do'stda bonus beriladi
                # (masalan 5 ta do'st = 1 kun, 10 ta do'st = yana 1 kun va h.k.)
                if total_referrals % REFERRALS_NEEDED_PER_BONUS == 0:
                    referrer = await db.get_user(referrer_id)
                    referrer_lang = referrer["language"] if referrer else "uz"
                    await db.add_premium_days(referrer_id, REFERRAL_BONUS_DAYS)
                    try:
                        await bot.send_message(
                            referrer_id,
                            t("referral_bonus_received", referrer_lang, days=REFERRAL_BONUS_DAYS),
                        )
                    except Exception:
                        pass
        await _show_main_menu(message, lang)
        return

    # ---- Anonim xabar yozish (t.me/bot?start=<owner_id>) ----
    if not payload.isdigit():
        await _show_main_menu(message, lang)
        return

    owner_id = int(payload)

    if owner_id == message.from_user.id:
        await message.answer(t("cannot_message_self", lang))
        await _show_main_menu(message, lang)
        return

    owner = await db.get_user(owner_id)
    if not owner:
        await _show_main_menu(message, lang)
        return

    owner_name = owner["full_name"] or (f"@{owner['username']}" if owner["username"] else "user")
    await state.update_data(target_user_id=owner_id)
    await state.set_state(AnonMessageStates.waiting_for_message)
    await message.answer(t("ask_message_to_owner", lang, name=owner_name))


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]
    await _show_main_menu(message, lang)


async def _show_main_menu(message: Message, lang: str):
    await message.answer(
        t("welcome", lang, name=message.from_user.full_name),
        reply_markup=main_menu_keyboard(lang, message.from_user.id),
    )


# ---------- Til tanlash ----------

@router.message(F.text.in_({t("main_menu_language", "uz"), t("main_menu_language", "en"), t("main_menu_language", "ru")}))
async def choose_language_menu(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    await message.answer(t("choose_language", user["language"]), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def set_language_callback(callback: CallbackQuery):
    lang = callback.data.split(":", 1)[1]
    await db.set_language(callback.from_user.id, lang)
    await callback.message.edit_text(t("language_set", lang))
    await callback.message.answer(
        t("welcome", lang, name=callback.from_user.full_name),
        reply_markup=main_menu_keyboard(lang, callback.from_user.id),
    )
    await callback.answer()


# ---------- Mening havolam ----------

@router.message(F.text.in_({t("main_menu_link", "uz"), t("main_menu_link", "en"), t("main_menu_link", "ru")}))
async def my_link(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]
    link = f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"
    await message.answer(t("your_link", lang, link=link))


# ---------- Statistikam ----------

@router.message(F.text.in_({t("main_menu_stats", "uz"), t("main_menu_stats", "en"), t("main_menu_stats", "ru")}))
async def my_stats(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]
    stats = await db.get_user_stats(message.from_user.id)
    joined = (user["created_at"] or "")[:10]
    text = t(
        "stats_title",
        lang,
        received=stats["received"],
        answered=stats["answered"],
        joined=joined,
    )

    if await db.is_premium_active(message.from_user.id):
        adv = await db.get_advanced_user_stats(message.from_user.id)
        top_reaction = adv["top_reaction"] or t("no_reactions_yet", lang)
        text += t(
            "stats_advanced",
            lang,
            total_reactions=adv["total_reactions"],
            top_reaction=top_reaction,
            reply_rate=adv["reply_rate"],
        )

    await message.answer(text)

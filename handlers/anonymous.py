from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database as db
from keyboards import message_action_keyboard, main_menu_keyboard
from locales.texts import t
from states import AnonMessageStates

router = Router(name="anonymous")


def _content_preview(message: Message) -> str:
    """Ma'lumotlar bazasida saqlash va admin panelda ko'rsatish uchun qisqa matn."""
    if message.text:
        return message.text
    if message.caption:
        return message.caption

    mapping = {
        "photo": "📷 [Rasm]",
        "video": "🎥 [Video]",
        "animation": "🎞 [GIF]",
        "sticker": "🌟 [Stiker]",
        "voice": "🎤 [Ovozli xabar]",
        "video_note": "⭕ [Doira video]",
        "document": "📎 [Fayl]",
        "audio": "🎵 [Audio]",
    }
    return mapping.get(message.content_type, f"[{message.content_type}]")


async def _relay(bot: Bot, target_id: int, source: Message,
                  header_text_key: str, header_text_key_media: str,
                  lang: str, keyboard) -> None:
    """Xabarni (matn yoki media) boshqa foydalanuvchiga anonim tarzda yetkazadi."""
    if source.content_type == "text":
        await bot.send_message(
            target_id,
            t(header_text_key, lang, text=source.text),
            reply_markup=keyboard,
        )
    else:
        # Avval qisqa sarlavha, keyin asl kontent (rasm/video/gif/stiker/...) o'zgarishsiz ko'chiriladi.
        # copy_to "kimdan kelgani" haqida hech qanday iz qoldirmaydi — anonimlik saqlanadi.
        await bot.send_message(target_id, t(header_text_key_media, lang))
        await source.copy_to(target_id, reply_markup=keyboard)


@router.message(AnonMessageStates.waiting_for_message)
async def receive_anon_message(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    owner_id = data.get("target_user_id")
    await state.clear()

    sender = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = sender["language"]

    if not owner_id:
        await message.answer(t("welcome", lang, name=message.from_user.full_name),
                              reply_markup=main_menu_keyboard(lang, message.from_user.id))
        return

    preview = _content_preview(message)
    msg_id = await db.save_message(message.from_user.id, owner_id, preview)

    owner = await db.get_user(owner_id)
    owner_lang = owner["language"] if owner else "uz"

    # Birinchi xabar — qabul qiluvchi hali yuboruvchini bilmaydi, shuning uchun
    # "kim yozganini ko'rish" tugmasi ko'rsatiladi.
    keyboard = message_action_keyboard(owner_lang, msg_id, include_reveal=True)

    try:
        await _relay(bot, owner_id, message, "new_anonymous_message",
                     "new_anonymous_message_media", owner_lang, keyboard)
    except Exception:
        # Owner botni bloklagan yoki chat topilmadi bo'lishi mumkin — jim o'tkazamiz
        pass

    await message.answer(t("message_sent_to_owner", lang),
                          reply_markup=main_menu_keyboard(lang, message.from_user.id))


@router.callback_query(F.data.startswith("reply:"))
async def start_reply(callback: CallbackQuery, state: FSMContext):
    message_id = int(callback.data.split(":", 1)[1])
    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]

    await state.update_data(reply_to_message_id=message_id)
    await state.set_state(AnonMessageStates.waiting_for_reply)
    await callback.message.answer(t("ask_reply_text", lang))
    await callback.answer()


@router.message(AnonMessageStates.waiting_for_reply)
async def send_reply(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    original_id = data.get("reply_to_message_id")
    await state.clear()

    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    original = await db.get_message(original_id) if original_id else None
    if not original:
        await message.answer(t("reply_sent", lang), reply_markup=main_menu_keyboard(lang, message.from_user.id))
        return

    original_sender_id = original["sender_id"]
    preview = _content_preview(message)
    new_msg_id = await db.save_message(message.from_user.id, original_sender_id, preview,
                                        is_reply=True, parent_id=original_id)

    recipient = await db.get_user(original_sender_id)
    recipient_lang = recipient["language"] if recipient else "uz"

    # Javob zanjirida ikkala taraf ham allaqachon bir-birini bilishadi (kontekstdan),
    # shuning uchun "kim yozganini ko'rish" tugmasi kerak emas — faqat "Javob berish"
    # tugmasi bo'ladi, shu orqali suhbat cheksiz davom etaveradi.
    keyboard = message_action_keyboard(recipient_lang, new_msg_id, include_reveal=False)

    try:
        await _relay(bot, original_sender_id, message, "you_got_reply",
                     "you_got_reply_media", recipient_lang, keyboard)
    except Exception:
        pass

    await message.answer(t("reply_sent", lang), reply_markup=main_menu_keyboard(lang, message.from_user.id))


@router.callback_query(F.data.startswith("reveal:"))
async def reveal_sender(callback: CallbackQuery):
    message_id = int(callback.data.split(":", 1)[1])
    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]

    is_premium = await db.is_premium_active(callback.from_user.id)
    if not is_premium:
        await callback.answer(t("reveal_locked", lang), show_alert=True)
        return

    original = await db.get_message(message_id)
    if not original or original["receiver_id"] != callback.from_user.id:
        await callback.answer()
        return

    sender = await db.get_user(original["sender_id"])
    if sender and sender["username"]:
        who = f"@{sender['username']}"
    elif sender:
        who = sender["full_name"] or t("unknown_username", lang, id=sender["telegram_id"])
    else:
        who = t("unknown_username", lang, id=original["sender_id"])

    if sender and await db.is_premium_active(sender["telegram_id"]):
        who = f"{who} {t('premium_badge', lang)}"

    await callback.answer(t("reveal_result", lang, who=who), show_alert=True)


@router.callback_query(F.data.startswith("react:"))
async def react_to_message(callback: CallbackQuery):
    _, message_id, emoji = callback.data.split(":", 2)
    await db.set_reaction(int(message_id), emoji)

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    await callback.answer(t("react_saved", user["language"]))

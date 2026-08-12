from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database as db
from keyboards import message_action_keyboard, main_menu_keyboard
from locales.texts import t
from states import AnonMessageStates

router = Router(name="anonymous")


@router.message(AnonMessageStates.waiting_for_message, F.text)
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

    msg_id = await db.save_message(message.from_user.id, owner_id, message.text)

    owner = await db.get_user(owner_id)
    owner_lang = owner["language"] if owner else "uz"
    owner_is_premium = await db.is_premium_active(owner_id)

    try:
        await bot.send_message(
            owner_id,
            t("new_anonymous_message", owner_lang, text=message.text),
            reply_markup=message_action_keyboard(owner_lang, msg_id, owner_is_premium),
        )
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


@router.message(AnonMessageStates.waiting_for_reply, F.text)
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
    await db.save_message(message.from_user.id, original_sender_id, message.text,
                           is_reply=True, parent_id=original_id)

    sender = await db.get_user(original_sender_id)
    sender_lang = sender["language"] if sender else "uz"
    try:
        await bot.send_message(
            original_sender_id,
            t("you_got_reply", sender_lang, text=message.text),
        )
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

    await callback.answer(t("reveal_result", lang, who=who), show_alert=True)


@router.callback_query(F.data.startswith("react:"))
async def react_to_message(callback: CallbackQuery):
    _, message_id, emoji = callback.data.split(":", 2)
    await db.set_reaction(int(message_id), emoji)

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    await callback.answer(t("react_saved", user["language"]))

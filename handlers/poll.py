from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database as db
from keyboards import main_menu_keyboard
from locales.texts import t
from states import PollStates

router = Router(name="poll")

MIN_OPTIONS = 2
MAX_OPTIONS = 10


@router.message(F.text.in_({t("main_menu_poll", "uz"), t("main_menu_poll", "en"), t("main_menu_poll", "ru")}))
async def poll_menu(message: Message, state: FSMContext):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    if not await db.is_premium_active(message.from_user.id):
        await message.answer(t("poll_locked", lang))
        return

    await state.set_state(PollStates.waiting_for_question)
    await message.answer(t("poll_ask_question", lang))


@router.message(PollStates.waiting_for_question, F.text)
async def poll_receive_question(message: Message, state: FSMContext):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    await state.update_data(question=message.text)
    await state.set_state(PollStates.waiting_for_options)
    await message.answer(t("poll_ask_options", lang))


@router.message(PollStates.waiting_for_options, F.text)
async def poll_receive_options(message: Message, state: FSMContext, bot: Bot):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    options = [opt.strip() for opt in message.text.split(",") if opt.strip()]

    if len(options) < MIN_OPTIONS:
        await message.answer(t("poll_too_few_options", lang))
        return
    if len(options) > MAX_OPTIONS:
        await message.answer(t("poll_too_many_options", lang))
        return

    data = await state.get_data()
    question = data.get("question", "")
    await state.clear()

    try:
        await bot.send_poll(
            chat_id=message.from_user.id,
            question=question,
            options=options,
            is_anonymous=True,
        )
        await db.save_poll(message.from_user.id, question)
        await message.answer(
            t("poll_created", lang), reply_markup=main_menu_keyboard(lang, message.from_user.id)
        )
    except Exception:
        await message.answer(
            t("poll_error", lang), reply_markup=main_menu_keyboard(lang, message.from_user.id)
        )

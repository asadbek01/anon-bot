from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database as db
from config import ADMIN_IDS
from keyboards import main_menu_keyboard
from locales.texts import t
from states import AdStates

router = Router(name="ads")


@router.message(F.text.in_({t("main_menu_ads", "uz"), t("main_menu_ads", "en"), t("main_menu_ads", "ru")}))
async def ads_menu(message: Message, state: FSMContext):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]
    await state.set_state(AdStates.waiting_for_ad_message)
    await message.answer(t("ask_ad_message", lang))


@router.message(AdStates.waiting_for_ad_message, F.text)
async def receive_ad_message(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    who = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                t("new_ad_message", "uz", who=who, id=message.from_user.id, text=message.text),
            )
        except Exception:
            # Admin botni bloklagan yoki chat topilmagan bo'lishi mumkin — jim o'tkazamiz
            pass

    await message.answer(t("ad_sent", lang), reply_markup=main_menu_keyboard(lang, message.from_user.id))

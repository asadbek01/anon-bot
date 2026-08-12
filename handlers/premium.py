import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice

import database as db
from config import PREMIUM_PLANS
from keyboards import premium_plans_keyboard, payment_method_keyboard
from locales.texts import t

router = Router(name="premium")


@router.message(F.text.in_({t("main_menu_premium", "uz"), t("main_menu_premium", "en"), t("main_menu_premium", "ru")}))
async def premium_menu(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]
    await message.answer(_premium_info_text(user, lang), reply_markup=premium_plans_keyboard(lang))


@router.callback_query(F.data == "premium_back")
async def premium_back(callback: CallbackQuery):
    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]
    await callback.message.edit_text(_premium_info_text(user, lang), reply_markup=premium_plans_keyboard(lang))
    await callback.answer()


def _premium_info_text(user: dict, lang: str) -> str:
    is_active = bool(user["is_premium"]) and user["premium_until"] and \
        datetime.datetime.fromisoformat(user["premium_until"]) > datetime.datetime.utcnow()
    if is_active:
        until = datetime.datetime.fromisoformat(user["premium_until"])
        # Agar muddat 50 yildan ko'p bo'lsa — "Butunlay" deb ko'rsatamiz
        if until.year - datetime.datetime.utcnow().year > 50:
            status = t("premium_active_until", lang, date="♾")
        else:
            status = t("premium_active_until", lang, date=until.strftime("%d.%m.%Y"))
    else:
        status = t("premium_not_active", lang)
    return t("premium_info", lang, status=status)


@router.callback_query(F.data.startswith("premium_plan:"))
async def choose_plan(callback: CallbackQuery):
    plan_key = callback.data.split(":", 1)[1]
    if plan_key not in PREMIUM_PLANS:
        await callback.answer()
        return

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]
    plan_label = t(f"plan_{plan_key}", lang, **_plan_fmt(plan_key))

    await callback.message.edit_text(
        t("choose_payment_method", lang, plan=plan_label),
        reply_markup=payment_method_keyboard(lang, plan_key),
    )
    await callback.answer()


def _plan_fmt(plan_key: str) -> dict:
    plan = PREMIUM_PLANS[plan_key]
    return {"stars": plan["stars"], "uzs": f"{plan['uzs']:,}".replace(",", " ")}


@router.callback_query(F.data.startswith("pay:stars:"))
async def pay_with_stars(callback: CallbackQuery, bot: Bot):
    plan_key = callback.data.split(":", 2)[2]
    if plan_key not in PREMIUM_PLANS:
        await callback.answer()
        return
    plan = PREMIUM_PLANS[plan_key]

    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=t("invoice_title", lang),
        description=t("invoice_description", lang, days=plan["days"] if plan["days"] < 36500 else "∞"),
        payload=f"premium:{plan_key}",
        provider_token="",  # Telegram Stars uchun bo'sh qoldiriladi
        currency="XTR",
        prices=[LabeledPrice(label=t("invoice_title", lang), amount=plan["stars"])],
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay:click:"))
@router.callback_query(F.data.startswith("pay:payme:"))
async def pay_with_click_or_payme(callback: CallbackQuery):
    """Click va Payme hozircha ulanmagan — foydalanuvchiga o'z tilida
    'tez orada' xabarini ko'rsatamiz."""
    user = await db.get_or_create_user(
        callback.from_user.id, callback.from_user.username, callback.from_user.full_name
    )
    lang = user["language"]
    await callback.answer(t("payment_coming_soon", lang), show_alert=True)


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    payload = message.successful_payment.invoice_payload
    plan_key = payload.split(":", 1)[1] if payload.startswith("premium:") else "30d"
    plan = PREMIUM_PLANS.get(plan_key, PREMIUM_PLANS["30d"])
    days = plan["days"]

    await db.save_payment(
        message.from_user.id,
        amount=str(message.successful_payment.total_amount),
        currency=message.successful_payment.currency,
        method="stars",
        status="paid",
        transaction_id=message.successful_payment.telegram_payment_charge_id,
    )
    await db.set_premium(message.from_user.id, days)

    shown_days = "∞" if days >= 36500 else days
    await message.answer(t("payment_success", lang, days=shown_days))

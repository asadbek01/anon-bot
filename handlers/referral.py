from aiogram import Router, F
from aiogram.types import Message

import database as db
from config import BOT_USERNAME, REFERRAL_BONUS_DAYS, REFERRALS_NEEDED_PER_BONUS
from locales.texts import t

router = Router(name="referral")


@router.message(F.text.in_({t("main_menu_referral", "uz"), t("main_menu_referral", "en"), t("main_menu_referral", "ru")}))
async def referral_menu(message: Message):
    user = await db.get_or_create_user(
        message.from_user.id, message.from_user.username, message.from_user.full_name
    )
    lang = user["language"]

    link = f"https://t.me/{BOT_USERNAME}?start=ref{message.from_user.id}"
    count = await db.get_referral_count(message.from_user.id)
    bonus_days = (count // REFERRALS_NEEDED_PER_BONUS) * REFERRAL_BONUS_DAYS
    remaining = REFERRALS_NEEDED_PER_BONUS - (count % REFERRALS_NEEDED_PER_BONUS)

    await message.answer(
        t(
            "referral_info",
            lang,
            days=REFERRAL_BONUS_DAYS,
            needed=REFERRALS_NEEDED_PER_BONUS,
            link=link,
            count=count,
            bonus_days=bonus_days,
            remaining=remaining,
        )
    )

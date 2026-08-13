"""
Barcha foydalanuvchiga ko'rinadigan matnlar shu yerda, uch til uchun.
Yangi matn qo'shmoqchi bo'lsang, shu dict ichiga uz/en/ru variantlarini qo'sh.
"""

TEXTS = {
    "choose_language": {
        "uz": "🌐 Tilni tanlang:",
        "en": "🌐 Choose your language:",
        "ru": "🌐 Выберите язык:",
    },
    "language_set": {
        "uz": "✅ Til o'zbekcha qilib tanlandi.",
        "en": "✅ Language set to English.",
        "ru": "✅ Язык изменён на русский.",
    },
    "welcome": {
        "uz": (
            "👋 Assalomu alaykum, {name}!\n\n"
            "Bu bot orqali senga <b>anonim</b> tarzda savol, fikr yoki e'tirof yozishlari mumkin.\n"
            "Pastdagi menyudan foydalan 👇"
        ),
        "en": (
            "👋 Hello, {name}!\n\n"
            "With this bot, people can send you <b>anonymous</b> questions, thoughts or confessions.\n"
            "Use the menu below 👇"
        ),
        "ru": (
            "👋 Привет, {name}!\n\n"
            "Через этого бота тебе могут писать <b>анонимные</b> вопросы, мысли или признания.\n"
            "Используй меню ниже 👇"
        ),
    },
    "main_menu_link": {
        "uz": "🔗 Mening havolam",
        "en": "🔗 My link",
        "ru": "🔗 Моя ссылка",
    },
    "main_menu_premium": {
        "uz": "💎 Premium",
        "en": "💎 Premium",
        "ru": "💎 Премиум",
    },
    "main_menu_language": {
        "uz": "🌐 Til",
        "en": "🌐 Language",
        "ru": "🌐 Язык",
    },
    "main_menu_stats": {
        "uz": "📊 Statistikam",
        "en": "📊 My stats",
        "ru": "📊 Моя статистика",
    },
    "main_menu_admin": {
        "uz": "🛠 Admin panel",
        "en": "🛠 Admin panel",
        "ru": "🛠 Админ-панель",
    },
    "main_menu_ads": {
        "uz": "📢 Reklama",
        "en": "📢 Advertising",
        "ru": "📢 Реклама",
    },
    "ask_ad_message": {
        "uz": (
            "📢 <b>Reklama bo'limi</b>\n\n"
            "Reklama taklifingiz yoki hamkorlik bo'yicha xabaringizni yozing — "
            "u to'g'ridan-to'g'ri administratorga yuboriladi."
        ),
        "en": (
            "📢 <b>Advertising</b>\n\n"
            "Write your ad proposal or partnership message — "
            "it will be sent directly to the administrator."
        ),
        "ru": (
            "📢 <b>Реклама</b>\n\n"
            "Напиши своё рекламное предложение или сообщение о сотрудничестве — "
            "оно будет отправлено напрямую администратору."
        ),
    },
    "ad_sent": {
        "uz": "✅ Xabaringiz administratorga yuborildi. Tez orada siz bilan bog'lanishadi!",
        "en": "✅ Your message has been sent to the administrator. They'll contact you soon!",
        "ru": "✅ Твоё сообщение отправлено администратору. С тобой скоро свяжутся!",
    },
    "new_ad_message": {
        "uz": (
            "📢 <b>Yangi reklama so'rovi</b>\n\n"
            "👤 Kimdan: {who}\n"
            "🆔 ID: <code>{id}</code>\n\n"
            "✉️ Xabar:\n{text}"
        ),
        "en": (
            "📢 <b>New advertising inquiry</b>\n\n"
            "👤 From: {who}\n"
            "🆔 ID: <code>{id}</code>\n\n"
            "✉️ Message:\n{text}"
        ),
        "ru": (
            "📢 <b>Новый рекламный запрос</b>\n\n"
            "👤 От: {who}\n"
            "🆔 ID: <code>{id}</code>\n\n"
            "✉️ Сообщение:\n{text}"
        ),
    },
    "your_link": {
        "uz": (
            "🔗 <b>Sening shaxsiy havolang:</b>\n"
            "<code>{link}</code>\n\n"
            "Shu havolani story, bio yoki do'stlaringga yubor — ular orqali senga "
            "anonim xabar yoza olishadi."
        ),
        "en": (
            "🔗 <b>Your personal link:</b>\n"
            "<code>{link}</code>\n\n"
            "Share this link in your story, bio, or with friends — they'll be able "
            "to send you anonymous messages."
        ),
        "ru": (
            "🔗 <b>Твоя личная ссылка:</b>\n"
            "<code>{link}</code>\n\n"
            "Поделись этой ссылкой в истории, био или с друзьями — они смогут "
            "присылать тебе анонимные сообщения."
        ),
    },
    "ask_message_to_owner": {
        "uz": "✍️ {name} ga anonim xabaringizni yozing:",
        "en": "✍️ Write your anonymous message to {name}:",
        "ru": "✍️ Напиши анонимное сообщение для {name}:",
    },
    "cannot_message_self": {
        "uz": "🙂 Bu — sening o'z havolang. Uni boshqalarga yubor.",
        "en": "🙂 This is your own link. Share it with others instead.",
        "ru": "🙂 Это твоя собственная ссылка. Поделись ей с другими.",
    },
    "message_sent_to_owner": {
        "uz": "✅ Xabaringiz anonim tarzda yuborildi!",
        "en": "✅ Your message has been sent anonymously!",
        "ru": "✅ Твоё сообщение отправлено анонимно!",
    },
    "new_anonymous_message": {
        "uz": "📩 <b>Senga anonim xabar keldi:</b>\n\n{text}",
        "en": "📩 <b>You received an anonymous message:</b>\n\n{text}",
        "ru": "📩 <b>Тебе пришло анонимное сообщение:</b>\n\n{text}",
    },
    "new_anonymous_message_media": {
        "uz": "📩 <b>Senga anonim xabar keldi:</b>",
        "en": "📩 <b>You received an anonymous message:</b>",
        "ru": "📩 <b>Тебе пришло анонимное сообщение:</b>",
    },
    "reply_button": {
        "uz": "↩️ Javob berish",
        "en": "↩️ Reply",
        "ru": "↩️ Ответить",
    },
    "reveal_button": {
        "uz": "🕵️ Kim yozganini ko'rish",
        "en": "🕵️ See who sent this",
        "ru": "🕵️ Узнать, кто написал",
    },
    "reveal_locked": {
        "uz": (
            "🔒 Bu funksiya faqat <b>Premium</b> foydalanuvchilar uchun.\n"
            "Premium sotib olib, senga kim yozganini bilib ol!"
        ),
        "en": (
            "🔒 This feature is only for <b>Premium</b> users.\n"
            "Get Premium to see who's writing to you!"
        ),
        "ru": (
            "🔒 Эта функция доступна только <b>Премиум</b> пользователям.\n"
            "Оформи Премиум, чтобы узнать, кто тебе пишет!"
        ),
    },
    "reveal_result": {
        "uz": "🕵️ <b>Yuboruvchi:</b> {who}",
        "en": "🕵️ <b>Sender:</b> {who}",
        "ru": "🕵️ <b>Отправитель:</b> {who}",
    },
    "unknown_username": {
        "uz": "username yo'q, ID: {id}",
        "en": "no username, ID: {id}",
        "ru": "нет username, ID: {id}",
    },
    "ask_reply_text": {
        "uz": "✍️ Javobingizni yozing:",
        "en": "✍️ Write your reply:",
        "ru": "✍️ Напиши свой ответ:",
    },
    "reply_sent": {
        "uz": "✅ Javobingiz yuborildi.",
        "en": "✅ Your reply has been sent.",
        "ru": "✅ Твой ответ отправлен.",
    },
    "you_got_reply": {
        "uz": "✉️ <b>Sizning xabaringizga javob keldi:</b>\n\n{text}",
        "en": "✉️ <b>You got a reply to your message:</b>\n\n{text}",
        "ru": "✉️ <b>Пришёл ответ на твоё сообщение:</b>\n\n{text}",
    },
    "you_got_reply_media": {
        "uz": "✉️ <b>Sizning xabaringizga javob keldi:</b>",
        "en": "✉️ <b>You got a reply to your message:</b>",
        "ru": "✉️ <b>Пришёл ответ на твоё сообщение:</b>",
    },
    "premium_info": {
        "uz": (
            "💎 <b>Premium imkoniyatlari:</b>\n\n"
            "🕵️ Senga kim yozganini ko'rish\n"
            "🎭 Vanish mode — xabar o'qilgach o'chib ketadi\n"
            "🏅 Ismingiz yonida maxsus belgi\n"
            "📊 Kengaytirilgan statistika\n\n"
            "{status}\n\n"
            "Muddatni tanlang 👇"
        ),
        "en": (
            "💎 <b>Premium features:</b>\n\n"
            "🕵️ See who's writing to you\n"
            "🎭 Vanish mode — messages disappear after being read\n"
            "🏅 Special badge next to your name\n"
            "📊 Advanced statistics\n\n"
            "{status}\n\n"
            "Choose a duration 👇"
        ),
        "ru": (
            "💎 <b>Возможности Премиум:</b>\n\n"
            "🕵️ Видеть, кто тебе пишет\n"
            "🎭 Vanish mode — сообщения исчезают после прочтения\n"
            "🏅 Специальный значок рядом с именем\n"
            "📊 Расширенная статистика\n\n"
            "{status}\n\n"
            "Выбери срок 👇"
        ),
    },
    "plan_1d": {"uz": "1 kun — {stars}⭐ / {uzs} so'm", "en": "1 day — {stars}⭐ / {uzs} UZS", "ru": "1 день — {stars}⭐ / {uzs} сум"},
    "plan_7d": {"uz": "7 kun — {stars}⭐ / {uzs} so'm", "en": "7 days — {stars}⭐ / {uzs} UZS", "ru": "7 дней — {stars}⭐ / {uzs} сум"},
    "plan_30d": {"uz": "1 oy — {stars}⭐ / {uzs} so'm", "en": "1 month — {stars}⭐ / {uzs} UZS", "ru": "1 месяц — {stars}⭐ / {uzs} сум"},
    "plan_lifetime": {"uz": "♾ Butunlay — {stars}⭐ / {uzs} so'm", "en": "♾ Forever — {stars}⭐ / {uzs} UZS", "ru": "♾ Навсегда — {stars}⭐ / {uzs} сум"},
    "choose_payment_method": {
        "uz": "💳 <b>{plan}</b>\n\nTo'lov usulini tanlang:",
        "en": "💳 <b>{plan}</b>\n\nChoose a payment method:",
        "ru": "💳 <b>{plan}</b>\n\nВыбери способ оплаты:",
    },
    "payment_coming_soon": {
        "uz": "🚧 Bu to'lov usuli tez orada ishga tushadi. Hozircha ⭐ Stars orqali to'lashingiz mumkin.",
        "en": "🚧 This payment method is coming soon. For now, you can pay with ⭐ Stars.",
        "ru": "🚧 Этот способ оплаты скоро появится. Пока можно оплатить через ⭐ Stars.",
    },
    "premium_active_until": {
        "uz": "✅ Sizda Premium faol, muddati: {date} gacha",
        "en": "✅ You have active Premium until: {date}",
        "ru": "✅ У тебя активен Премиум до: {date}",
    },
    "premium_not_active": {
        "uz": "❌ Hozircha Premium faol emas.",
        "en": "❌ Premium is not active yet.",
        "ru": "❌ Премиум пока не активен.",
    },
    "pay_with_stars": {
        "uz": "⭐ Stars orqali sotib olish",
        "en": "⭐ Buy with Stars",
        "ru": "⭐ Купить за Stars",
    },
    "pay_with_click": {
        "uz": "💳 Click orqali",
        "en": "💳 Pay with Click",
        "ru": "💳 Оплатить через Click",
    },
    "pay_with_payme": {
        "uz": "💳 Payme orqali",
        "en": "💳 Pay with Payme",
        "ru": "💳 Оплатить через Payme",
    },
    "invoice_title": {
        "uz": "Premium obuna",
        "en": "Premium subscription",
        "ru": "Премиум подписка",
    },
    "invoice_description": {
        "uz": "{days} kunlik Premium obuna",
        "en": "{days}-day Premium subscription",
        "ru": "Премиум подписка на {days} дней",
    },
    "payment_success": {
        "uz": "🎉 To'lov muvaffaqiyatli! Premium {days} kunga faollashtirildi.",
        "en": "🎉 Payment successful! Premium activated for {days} days.",
        "ru": "🎉 Оплата прошла успешно! Премиум активирован на {days} дней.",
    },
    "click_link_ready": {
        "uz": "💳 To'lov havolasi tayyor, quyidagi tugma orqali to'lang:",
        "en": "💳 Your payment link is ready, pay via the button below:",
        "ru": "💳 Ссылка на оплату готова, оплати через кнопку ниже:",
    },
    "stats_title": {
        "uz": (
            "📊 <b>Sening statistikang:</b>\n\n"
            "📩 Qabul qilingan xabarlar: {received}\n"
            "↩️ Javob berilgan: {answered}\n"
            "📅 Ro'yxatdan o'tgan sana: {joined}"
        ),
        "en": (
            "📊 <b>Your stats:</b>\n\n"
            "📩 Messages received: {received}\n"
            "↩️ Replied: {answered}\n"
            "📅 Joined on: {joined}"
        ),
        "ru": (
            "📊 <b>Твоя статистика:</b>\n\n"
            "📩 Получено сообщений: {received}\n"
            "↩️ Отвечено: {answered}\n"
            "📅 Дата регистрации: {joined}"
        ),
    },
    "stats_advanced": {
        "uz": (
            "\n\n💎 <b>Kengaytirilgan (Premium):</b>\n"
            "😀 Jami reaksiyalar: {total_reactions}\n"
            "🔥 Eng ko'p tushgan reaksiya: {top_reaction}\n"
            "📈 Javob berish foizi: {reply_rate}%"
        ),
        "en": (
            "\n\n💎 <b>Advanced (Premium):</b>\n"
            "😀 Total reactions: {total_reactions}\n"
            "🔥 Most common reaction: {top_reaction}\n"
            "📈 Reply rate: {reply_rate}%"
        ),
        "ru": (
            "\n\n💎 <b>Расширенная (Премиум):</b>\n"
            "😀 Всего реакций: {total_reactions}\n"
            "🔥 Самая частая реакция: {top_reaction}\n"
            "📈 Процент ответов: {reply_rate}%"
        ),
    },
    "no_reactions_yet": {
        "uz": "hali yo'q",
        "en": "none yet",
        "ru": "пока нет",
    },
    "premium_badge": {
        "uz": "💎",
        "en": "💎",
        "ru": "💎",
    },
    "back": {
        "uz": "⬅️ Orqaga",
        "en": "⬅️ Back",
        "ru": "⬅️ Назад",
    },
    "admin_not_allowed": {
        "uz": "⛔ Bu bo'lim faqat adminlar uchun.",
        "en": "⛔ This section is for admins only.",
        "ru": "⛔ Этот раздел только для администраторов.",
    },
    "admin_panel_title": {
        "uz": "🛠 <b>Admin panel</b>\n\nQuyidagilardan birini tanlang:",
        "en": "🛠 <b>Admin panel</b>\n\nChoose an option:",
        "ru": "🛠 <b>Админ-панель</b>\n\nВыбери один из пунктов:",
    },
    "admin_all_stats": {
        "uz": "📈 Umumiy statistika",
        "en": "📈 Overall stats",
        "ru": "📈 Общая статистика",
    },
    "admin_all_chats": {
        "uz": "💬 Barcha yozishmalar",
        "en": "💬 All conversations",
        "ru": "💬 Все переписки",
    },
    "admin_stats_text": {
        "uz": (
            "📈 <b>Umumiy statistika</b>\n\n"
            "👤 Foydalanuvchilar: {users}\n"
            "💎 Premium foydalanuvchilar: {premium}\n"
            "📩 Jami xabarlar: {messages}\n"
            "💰 Jami to'lovlar: {payments}"
        ),
        "en": (
            "📈 <b>Overall stats</b>\n\n"
            "👤 Users: {users}\n"
            "💎 Premium users: {premium}\n"
            "📩 Total messages: {messages}\n"
            "💰 Total payments: {payments}"
        ),
        "ru": (
            "📈 <b>Общая статистика</b>\n\n"
            "👤 Пользователей: {users}\n"
            "💎 Премиум пользователей: {premium}\n"
            "📩 Всего сообщений: {messages}\n"
            "💰 Всего платежей: {payments}"
        ),
    },
    "no_messages_yet": {
        "uz": "Hozircha xabarlar yo'q.",
        "en": "No messages yet.",
        "ru": "Пока нет сообщений.",
    },
    "react_saved": {
        "uz": "✅ Reaksiyangiz qabul qilindi!",
        "en": "✅ Your reaction was recorded!",
        "ru": "✅ Твоя реакция сохранена!",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Berilgan til uchun matnni qaytaradi, agar til topilmasa uz ishlatiladi."""
    entry = TEXTS.get(key, {})
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        return text.format(**kwargs)
    return text

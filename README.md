# 🤖 Anonim Savol-Javob Bot

Telegram uchun anonim savol-javob boti. Python + aiogram 3 + SQLite asosida qurilgan.

## ✨ Imkoniyatlar

- 🌐 3 til: O'zbekcha / English / Русский (birinchi kirishda tanlanadi)
- 🔗 Har bir foydalanuvchi uchun shaxsiy anonim havola (`t.me/bot?start=ID`)
- 📩 Anonim xabar yuborish va javob berish
- 😀 Xabarlarga tezkor emoji-reaksiya qo'yish
- 💎 **Premium**: kim yozganini ko'rish, ustuvor yetkazish, maxsus belgi
- 💳 To'lov: **Telegram Stars**, **Click**, **Payme**
- 🛠 **Admin panel**: umumiy statistika + barcha yozishmalarni (haqiqiy foydalanuvchilar bilan) ko'rish

## 📁 Loyiha tuzilishi

```
anon_qa_bot/
├── main.py                # Botni ishga tushirish
├── webhook_server.py       # Click/Payme to'lov tasdiqlarini qabul qiluvchi server
├── config.py                # .env dan sozlamalarni o'qiydi
├── database.py               # SQLite bilan ishlash (aiosqlite)
├── keyboards.py              # Barcha inline/reply klaviaturalar
├── states.py                 # FSM holatlari
├── locales/
│   └── texts.py               # uz/en/ru matnlari
├── handlers/
│   ├── start.py                # /start, til tanlash, shaxsiy havola
│   ├── anonymous.py            # Anonim xabar yuborish/javob/reveal/reaksiya
│   ├── premium.py              # Premium sotib olish (Stars/Click/Payme)
│   └── admin.py                # Admin panel
├── payments/
│   ├── click.py                 # Click to'lov havolasi
│   └── payme.py                 # Payme to'lov havolasi
├── requirements.txt
└── .env.example
```

## 🚀 Ishga tushirish

### 1. Muhitni tayyorlash

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. `.env` faylini sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va quyidagilarni to'ldiring:

- `BOT_TOKEN` — @BotFather dan olinadigan token
- `BOT_USERNAME` — botning username'i (masalan `mening_anon_botim`, `@` belgisiz)
- `ADMIN_IDS` — sizning Telegram ID'ingiz (bilmasangiz @userinfobot ga yozing)

### 3. Botni ishga tushirish

```bash
python main.py
```

Shu bilan bot ishlay boshlaydi: `/start` yozing, tilni tanlang, "🔗 Mening havolam" tugmasini bosib shaxsiy havolangizni oling va do'stlaringizga yuboring.

## ⭐ Telegram Stars orqali to'lovni yoqish

1. @BotFather ga o'ting → botingizni tanlang → **Payments**
2. Stars uchun alohida provider kerak emas — kod ichida tayyor (`currency="XTR"`)
3. `.env` da `PREMIUM_PRICE_STARS` — narxni Stars'da belgilang

## 💳 Click va Payme ni ulash (real to'lov uchun)

Bu ikkalasi ham **merchant hisob** va **ochiq HTTPS server** talab qiladi (test rejimida ham). Qadamlar:

### Click
1. https://merchant.click.uz da ro'yxatdan o'ting, servis yarating
2. `CLICK_MERCHANT_ID`, `CLICK_SERVICE_ID`, `CLICK_SECRET_KEY` larni oling va `.env` ga yozing
3. Click kabinetida **Callback URL** ni: `https://sizning-domeningiz.uz/click` qilib ko'rsating

### Payme
1. https://business.payme.uz da ro'yxatdan o'ting
2. `PAYME_MERCHANT_ID`, `PAYME_SECRET_KEY` larni `.env` ga yozing
3. Payme kabinetida webhook manzilini: `https://sizning-domeningiz.uz/payme` qilib ko'rsating

### Webhook serverni ishga tushirish

Bot bilan **parallel ravishda**, alohida terminalda:

```bash
python webhook_server.py
```

Bu server 8080-portda ishlaydi (`.env` dagi `WEBHOOK_PORT` orqali o'zgartiriladi). Uni internetga chiqarish uchun Nginx + SSL sertifikat (masalan Let's Encrypt) sozlashingiz kerak bo'ladi — bu qism sizning serveringiz sozlamalariga bog'liq.

> ⚠️ `webhook_server.py` ichidagi Payme qismi soddalashtirilgan skelet — production uchun Payme'ning to'liq holat-mashinasi (state machine) va tranzaksiyalarni alohida jadvalda saqlashni qo'shish tavsiya etiladi. Hujjat: https://developer.help.paycom.uz/

## 🎨 Qo'shimcha creativ g'oyalar (keyingi bosqich uchun)

Loyihaga keyinchalik qo'shsa bo'ladigan funksiyalar:

- 🗳 **Anonim so'rovnomalar** — foydalanuvchi o'z auditoriyasidan anonim ovoz yig'ishi
- 🏆 **Reyting/liderbord** — eng ko'p savol olganlar (ixtiyoriy, ochiq bo'lishi mumkin)
- 🎭 **"Kunlik savol" taklifi** — bot foydalanuvchiga tayyor savol variantlarini taklif qiladi
- 🔥 **Streak** — necha kun ketma-ket faol bo'lgani uchun belgilar
- 🖼 **Rasm/ovozli anonim xabarlar** — hozir faqat matn, kengaytirish mumkin
- 🌍 **Avtomatik tarjima** — agar yuboruvchi va qabul qiluvchi turli tilda bo'lsa, xabarni avtomatik tarjima qilib yuborish
- ⏳ **"Vanish mode"** — xabar o'qilgach, ma'lum vaqtdan keyin o'chib ketishi

## 🗃 Ma'lumotlar bazasi haqida eslatma

Loyiha **SQLite** (`bot.db` — bitta fayl) ishlatadi. Bu CSV bilan bir xil darajada oddiy (alohida server kerak emas), lekin:
- bir vaqtda ko'p yozuvlar bo'lsa ham fayl buzilmaydi,
- tezkor qidiruv va bog'liq jadvallar (users/messages/payments) qulay ishlaydi.

Agar loyiha juda kattalashsa (o'nlab minglab foydalanuvchi), kelajakda `database.py` dagi so'rovlarni deyarli o'zgarishsiz PostgreSQL'ga ko'chirish mumkin.

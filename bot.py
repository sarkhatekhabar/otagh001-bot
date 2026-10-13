import os
import random
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# تنظیم گزارش خطا
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# دریافت امن توکن از GitHub Secrets
TOKEN = os.getenv("TOKEN")

# منوی اصلی ربات
MENU = ReplyKeyboardMarkup(
    [
        ["🎭 سرگرمی", "🧩 معما"],
        ["💡 ایده اینستاگرام", "✍️ کپشن"],
        ["🎬 سناریوی ویدئو", "ℹ️ راهنما"],
    ],
    resize_keyboard=True,
)

# معماها
RIDDLES = [
    ("آن چیست که هرچه از آن برداری بزرگ‌تر می‌شود؟", "گودال"),
    ("آن چیست که دندان دارد اما غذا نمی‌خورد؟", "شانه"),
    ("آن چیست که پا ندارد اما راه می‌رود؟", "آب"),
    ("چه چیزی مال توست اما دیگران بیشتر از تو از آن استفاده می‌کنند؟", "نام تو"),
    ("آن چیست که همیشه بالا می‌رود اما پایین نمی‌آید؟", "سن"),
]

# ایده‌های تولید محتوا
IDEAS = [
    "۳ اشتباه رایج که بیشتر مردم انجام می‌دهند را معرفی کن.",
    "یک داستان کوتاه با پایان غیرمنتظره بساز.",
    "۵ نکته کاربردی درباره موضوع موردعلاقه‌ات منتشر کن.",
    "یک باور اشتباه رایج را انتخاب کن و توضیح بده.",
    "یک چالش جذاب طراحی کن و از مخاطبان بخواه شرکت کنند.",
    "یک ویدئوی قبل و بعد با موضوعی جذاب بساز.",
    "یک سؤال بحث‌برانگیز اما محترمانه از مخاطبان بپرس.",
    "یک واقعیت عجیب و جالب را در قالب ویدئوی کوتاه تعریف کن.",
]

# کپشن‌های آماده
CAPTIONS = [
    "گاهی یک تصمیم کوچک، شروع یک تغییر بزرگ است. ✨",
    "قرار نیست کامل باشیم؛ کافی است هر روز بهتر شویم. 🌱",
    "نظرت چیه؟ تو هم تجربه مشابهی داشتی؟ 👇",
    "این پست رو برای کسی بفرست که بهش نیاز داره. ❤️",
    "از نظر تو مهم‌ترین نکته این موضوع چیه؟ 💬",
    "هر روز یک فرصت تازه برای بهتر شدن است. 🚀",
]

# الگوهای سناریوی ویدئو
SCENARIOS = [
    (
        "شروع: با یک سؤال کنجکاوکننده آغاز کن.\n"
        "میانه: سه نکته کوتاه و مفید بگو.\n"
        "پایان: از مخاطب بخواه نظرش را بنویسد."
    ),
    (
        "شروع: یک اشتباه رایج را نشان بده.\n"
        "میانه: راه درست را در چند مرحله توضیح بده.\n"
        "پایان: نتیجه را کوتاه و واضح جمع‌بندی کن."
    ),
    (
        "شروع: با یک جمله غافلگیرکننده آغاز کن.\n"
        "میانه: یک داستان کوتاه و جذاب تعریف کن.\n"
        "پایان: یک نتیجه جالب برای مخاطب داشته باش."
    ),
]


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    await update.effective_message.reply_text(
        "سلام! 👋 به اتاق ۰۰۱ خوش اومدی.\n\n"
        "اینجا می‌تونی معما حل کنی، بازی کنی و "
        "برای اینستاگرامت ایده و محتوا بگیری.\n\n"
        "از منوی زیر یک گزینه انتخاب کن.",
        reply_markup=MENU,
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        "به اتاق ۰۰۱ خوش اومدی! 🌟\n\n"
        "🧩 معما: حل معماهای کوتاه\n"
        "🎭 سرگرمی: بازی حدس عدد\n"
        "💡 ایده اینستاگرام: پیشنهاد ایده محتوا\n"
        "✍️ کپشن: دریافت متن آماده\n"
        "🎬 سناریو: دریافت طرح اولیه ویدئو\n\n"
        "برای شروع از دکمه‌های منو استفاده کن.",
        reply_markup=MENU,
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message

    if message is None or message.text is None:
        return

    text = message.text.strip()

    # انتخاب معما
    if text == "🧩 معما":
        riddle, answer = random.choice(RIDDLES)

        context.user_data["answer"] = answer
        context.user_data.pop("game", None)

        await message.reply_text(
            f"🧩 معمای تو:\n\n{riddle}\n\n"
            "جوابت رو بفرست!"
        )
        return

    # شروع بازی حدس عدد
    if text == "🎭 سرگرمی":
        context.user_data.pop("answer", None)
        context.user_data["game"] = True
        context.user_data["number"] = random.randint(1, 10)

        await message.reply_text(
            "🎭 بازی حدس عدد!\n\n"
            "من یک عدد بین ۱ تا ۱۰ انتخاب کردم.\n"
            "حدس بزن چه عددیه و برام بفرست."
        )
        return

    # تولید ایده
    if text == "💡 ایده اینستاگرام":
        context.user_data.pop("answer", None)
        context.user_data.pop("game", None)

        await message.reply_text(
            "💡 ایده پیشنهادی برای محتوا:\n\n"
            + random.choice(IDEAS),
            reply_markup=MENU,
        )
        return

    # تولید کپشن
    if text == "✍️ کپشن":
        context.user_data.pop("answer", None)
        context.user_data.pop("game", None)

        await message.reply_text(
            "✍️ کپشن پیشنهادی:\n\n"
            + random.choice(CAPTIONS),
            reply_markup=MENU,
        )
        return

    # تولید سناریو
    if text == "🎬 سناریوی ویدئو":
        context.user_data.pop("answer", None)
        context.user_data.pop("game", None)

        await message.reply_text(
            "🎬 سناریوی پیشنهادی ویدئو:\n\n"
            + random.choice(SCENARIOS),
            reply_markup=MENU,
        )
        return

    # نمایش راهنما
    if text == "ℹ️ راهنما":
        context.user_data.clear()
        await help_command(update, context)
        return

    # بررسی پاسخ معما
    if "answer" in context.user_data:
        answer = context.user_data.pop("answer")

        if text.casefold() == answer.casefold():
            await message.reply_text(
                "آفرین! 🎉 جواب درست بود.",
                reply_markup=MENU,
            )
        else:
            await message.reply_text(
                f"جواب درست «{answer}» بود. 😊",
                reply_markup=MENU,
            )
        return

    # بررسی بازی حدس عدد
    if context.user_data.get("game"):
        if not text.isdigit() or not 1 <= int(text) <= 10:
            await message.reply_text(
                "لطفاً یک عدد بین ۱ تا ۱۰ بفرست."
            )
            return

        guess = int(text)
        number = context.user_data["number"]

        if guess == number:
            context.user_data.pop("game", None)

            await message.reply_text(
                "🎉 آفرین! عدد رو درست حدس زدی.\n\n"
                "برای بازی دوباره روی «🎭 سرگرمی» بزن.",
                reply_markup=MENU,
            )

        elif guess < number:
            await message.reply_text(
                "عدد من بزرگ‌تره! دوباره حدس بزن."
            )

        else:
            await message.reply_text(
                "عدد من کوچک‌تره! دوباره حدس بزن."
            )

        return

    # پاسخ پیش‌فرض
    await message.reply_text(
        "برای استفاده از امکانات، یکی از گزینه‌های منو رو انتخاب کن. 👇",
        reply_markup=MENU,
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logging.error(
        "خطا هنگام پردازش درخواست",
        exc_info=context.error,
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "توکن تنظیم نشده است. مقدار TOKEN را در GitHub Secrets بررسی کن."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    app.add_error_handler(error_handler)

    logging.info("ربات اتاق ۰۰۱ آماده اجراست.")

    app.run_polling()


if __name__ == "__main__":
    main()




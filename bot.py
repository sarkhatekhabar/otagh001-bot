import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "توکن_ربات_را_اینجا_قرار_بده"

MENU = ReplyKeyboardMarkup(
    [
        ["🎭 سرگرمی", "🧩 معما"],
        ["💡 ایده اینستاگرام", "✍️ کپشن"],
        ["🎬 سناریوی ویدئو", "ℹ️ راهنما"],
    ],
    resize_keyboard=True,
)

RIDDLES = [
    ("آن چیست که هرچه از آن برداری بزرگ‌تر می‌شود؟", "گودال"),
    ("آن چیست که دندان دارد اما غذا نمی‌خورد؟", "شانه"),
    ("آن چیست که پا ندارد اما راه می‌رود؟", "آب"),
    ("چه چیزی مال توست اما دیگران بیشتر از تو از آن استفاده می‌کنند؟", "نام تو"),
]

IDEAS = [
    "۳ اشتباه رایج که بیشتر مردم انجام می‌دهند را معرفی کن.",
    "یک داستان کوتاه با پایان غیرمنتظره بساز.",
    "۵ نکته کاربردی درباره موضوع موردعلاقه‌ات منتشر کن.",
    "یک باور اشتباه رایج را انتخاب کن و توضیح بده.",
    "یک چالش جذاب طراحی کن و از مخاطبان بخواه شرکت کنند.",
    "قبل و بعد یک تغییر جالب را در قالب ویدئو نشان بده.",
]

CAPTIONS = [
    "گاهی یک تصمیم کوچک، شروع یک تغییر بزرگ است. ✨",
    "قرار نیست کامل باشیم؛ کافی است هر روز بهتر شویم. 🌱",
    "نظرت چیه؟ تو هم تجربه مشابهی داشتی؟ 👇",
    "این پست رو برای کسی بفرست که بهش نیاز داره. ❤️",
    "از نظر تو مهم‌ترین نکته این موضوع چیه؟ 💬",
]

SCENARIOS = [
    "شروع: یک سؤال کنجکاوکننده بپرس.\n"
    "میانه: سه نکته کوتاه و مفید بگو.\n"
    "پایان: از مخاطب بخواه نظرش را بنویسد.",

    "شروع: یک اشتباه رایج را نشان بده.\n"
    "میانه: راه درست را در چند مرحله توضیح بده.\n"
    "پایان: یک جمع‌بندی کوتاه ارائه کن.",

    "شروع: با یک جمله غافلگیرکننده آغاز کن.\n"
    "میانه: یک داستان کوتاه تعریف کن.\n"
    "پایان: نتیجه داستان را به مخاطب ربط بده.",
]


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "سلام! 👋 به اتاق ۰۰۱ خوش اومدی.\n\n"
        "از منوی زیر یکی از امکانات رو انتخاب کن.",
        reply_markup=MENU,
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text.strip()

    if text == "🧩 معما":
        riddle, answer = random.choice(RIDDLES)
        context.user_data["answer"] = answer
        await update.message.reply_text(
            f"🧩 معمای امروز:\n\n{riddle}\n\n"
            "جوابت رو بفرست!"
        )

    elif text == "🎭 سرگرمی":
        await update.message.reply_text(
            "🎭 بیا یک بازی کنیم!\n\n"
            "یک عدد از ۱ تا ۱۰ انتخاب کن و بفرست."
        )
        context.user_data["game"] = True

    elif text == "💡 ایده اینستاگرام":
        await update.message.reply_text(
            "💡 ایده پیشنهادی:\n\n"
            + random.choice(IDEAS)
        )

    elif text == "✍️ کپشن":
        await update.message.reply_text(
            "✍️ کپشن پیشنهادی:\n\n"
            + random.choice(CAPTIONS)
        )

    elif text == "🎬 سناریوی ویدئو":
        await update.message.reply_text(
            "🎬 سناریوی پیشنهادی:\n\n"
            + random.choice(SCENARIOS)
        )

    elif text == "ℹ️ راهنما":
        await update.message.reply_text(
            "راهنمای اتاق ۰۰۱:\n\n"
            "🧩 معما: حل معماهای کوتاه\n"
            "🎭 سرگرمی: بازی عددی\n"
            "💡 ایده: پیشنهاد ایده محتوا\n"
            "✍️ کپشن: متن آماده برای انتشار\n"
            "🎬 سناریو: طرح اولیه ویدئو",
            reply_markup=MENU,
        )

    elif "answer" in context.user_data:
        answer = context.user_data.pop("answer")
        if text.casefold() == answer.casefold():
            await update.message.reply_text(
                "آفرین! 🎉 جواب درست بود.",
                reply_markup=MENU,
            )
        else:
            await update.message.reply_text(
                f"جواب درست این بود: {answer}",
                reply_markup=MENU,
            )

    elif context.user_data.pop("game", False):
        if text.isdigit() and 1 <= int(text) <= 10:
            number = random.randint(1, 10)
            if int(text) == number:
                result = "عالیه! عدد رو درست حدس زدی! 🎉"
            else:
                result = f"عدد من {number} بود. دوباره امتحان کن!"
            await update.message.reply_text(
                result,
                reply_markup=MENU,
            )
        else:
            await update.message.reply_text(
                "لطفاً یک عدد بین ۱ تا ۱۰ بفرست.",
                reply_markup=MENU,
            )

    else:
        await update.message.reply_text(
            "یکی از گزینه‌های منو رو انتخاب کن.",
            reply_markup=MENU,
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Otagh 001 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()




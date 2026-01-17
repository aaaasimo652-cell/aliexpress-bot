import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEEPLINK = "https://s.click.aliexpress.com/e/_c3XgvtD"

def make_affiliate_link(url: str) -> str:
    return f"{DEEPLINK}?url={url}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا!\n\n"
        "🔗 صيفط رابط AliExpress\n"
        "🔥 نرجعو ليك رابط Affiliate ديالك"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if "aliexpress.com" not in text:
        await update.message.reply_text("❌ صيفط غير رابط AliExpress")
        return

    affiliate_link = make_affiliate_link(text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 رابط الشراء", url=affiliate_link)]
    ])

    await update.message.reply_text(
        "✅ هذا هو رابط Affiliate ديالك:",
        reply_markup=keyboard
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler

# 🔐 التوكن ديال البوت (ديرو فـ Render Environment Variable)
BOT_TOKEN = "8319614693:AAH2UBmAdOsiBDq5irxSuDufmNI5WFFtwNQ"

# 🔗 Deep Link ديال AliExpress Affiliate
DEEPLINK = "https://s.click.aliexpress.com/e/_c3XgvCtD"

def make_affiliate_link(url: str) -> str:
    return f"{DEEPLINK}?url={url}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا!\n\n"
        "🔗 صيفط أي رابط ديال AliExpress\n"
        "📦 وأنا نرجع ليك رابط Affiliate ديالك مباشرة 🔥"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if "aliexpress.com" not in text:
        await update.message.reply_text("❌ صيفط غير رابط صحيح ديال AliExpress")
        return

    affiliate_link = make_affiliate_link(text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 شراء بالرابط الذكي", url=affiliate_link)],
        [InlineKeyboardButton("📋 نسخ الرابط", url=affiliate_link)]
    ])

    await update.message.reply_text(
        "✅ تم إنشاء رابط Affiliate بنجاح:",
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

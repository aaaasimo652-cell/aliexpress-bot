import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

# حط deeplink ديال AliExpress ديالك
DEEP_LINK = "https://s.click.aliexpress.com/e/_C3XgYtD"

# ===== FUNCTIONS =====
def make_affiliate_link(url: str) -> str:
    return f"{DEEP_LINK}?url={url}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا بك\n"
        "🔗 صيفط رابط AliExpress\n"
        "💰 ونعطيك Affiliate link ديالك"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if "aliexpress.com" not in text:
        await update.message.reply_text("❌ صيفط رابط صحيح ديال AliExpress")
        return

    affiliate_link = make_affiliate_link(text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 الرابط ديالي", url=affiliate_link)]
    ])

    await update.message.reply_text(
        "✅ هادا هو Affiliate link ديالك:",
        reply_markup=keyboard
    )

# ===== HTTP SERVER (باش Koyeb يبقى خدام) =====
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

# ===== MAIN =====
def main():
    # شغل HTTP server فـ thread
    threading.Thread(target=run_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

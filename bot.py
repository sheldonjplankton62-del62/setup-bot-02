import os
from telegram import Update
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
ContextTypes,
filters,
)


# ===== CONFIG =====
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
raise SystemExit("BOT_TOKEN not set. Set environment variable BOT_TOKEN before running.")


# Pesan sambutan yang bisa disesuaikan
WELCOME_MESSAGE = os.getenv(
"WELCOME_MESSAGE",
"Selamat datang, {name}! 🎉 Kami harap kamu nyaman di grup ini. Harap patuhi aturan yang berlaku."
)


# ===== Handlers =====
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Halo! Bot aktif. Saya akan menyapa anggota baru di grup ini.")


async def greet_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
msg = update.effective_message
if not msg or not msg.new_chat_members:
return
for u in msg.new_chat_members:
try:
await msg.reply_text(WELCOME_MESSAGE.format(name=u.first_name or 'pengguna'))
except Exception as e:
print(f"Gagal mengirim pesan sambutan: {e}")


# ===== Main =====
def main():
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_members))
print("🤖 Bot berjalan — menyapa anggota baru di grup.")
app.run_polling()


if __name__ == "__main__":
main()

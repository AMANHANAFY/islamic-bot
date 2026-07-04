import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from gtts import gTTS

TOKEN = os.getenv("TOKEN")

# -------------------
# SIMPLE DATA
# -------------------

QURAN = [
    "Quran 96:1 Oku!",
    "Quran 39:9 Bilýänler bilen bilmeýänler deň däl",
    "Quran 20:114 Ylym artdyr"
]

HADITH = [
    "Ylym talap etmek farzdyr",
    "Ulamalar peygamberleriň mirasdarlarydyr"
]

# -------------------
# KHUTBA ENGINE
# -------------------

def build_khutba(topic):
    return f"""
🕌 KHUTBA

📌 Tema: {topic}

📖 Quran:
{chr(10).join(QURAN)}

📚 Hadith:
{chr(10).join(HADITH)}

🧠 Nesihat:
Ylym öwrenmek iň beýik amaldyr.
"""

# -------------------
# COMMANDS
# -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Islamic Bot Ready")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)
    if not topic:
        await update.message.reply_text("Tema ýaz")
        return

    await update.message.reply_text(build_khutba(topic))

async def khutba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)
    if not topic:
        await update.message.reply_text("Tema ýaz")
        return

    await update.message.reply_text(build_khutba(topic))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "salam" in text:
        await update.message.reply_text("Wa alaikum salam 🌙")
    else:
        await update.message.reply_text("Use /ask or /khutba")

# -------------------
# RUN BOT
# -------------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("khutba", khutba))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot started...")
app.run_polling()

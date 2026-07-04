import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
Sen hanafi mezhebine esaslanýan islami kömekçi botsyň.

Düzgünler:
- Salamlaş.
- Jogaplary Türkmen dilinde ýaz.
- Delil mümkin bolsa Quran we sahih hadysdan getir.
- Bilmeýän zadyň bolsa anyk aýt.
- Syýasy ýa-da ekstremistik mazmun döretme.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalamu alaikum 🌙\n\n"
       "Men AI Islamic Bot.\n"
       "Islendik islami soragy berip bilersiň."
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text("Soragyňy ýaz.\nMeselem:\n/ask Taharet näme?")
        return

    await update.message.chat.send_action("typing")

    prompt = SYSTEM_PROMPT + "\n\nUlanyjynyň soragy:\n" + question

    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text[:4096])
    except Exception as e:
        await update.message.reply_text(str(e))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.chat.send_action("typing")

    prompt = SYSTEM_PROMPT + "\n\nUlanyjy:\n" + text

    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text[:4096])
    except Exception:
        await update.message.reply_text("Ýalňyşlyk ýüze çykdy.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("AI Islamic Bot Started...")

app.run_polling()

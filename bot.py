from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a prompt to generate an image!")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    image = pipe(prompt).images[0]
    image.save("output.png")
    await update.message.reply_photo(photo=open("output.png", "rb"))

app = ApplicationBuilder().token("8203565510:AAGZxqRrZzu8boqqVZZG21jmkyfQ4v3xNdc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
app.run_polling()

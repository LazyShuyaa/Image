import requests
import base64
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your actual bot token
BOT_TOKEN = "8203565510:AAGZxqRrZzu8boqqVZZG21jmkyfQ4v3xNdc"
SD_API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a prompt and I'll generate an image using Stable Diffusion!")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("🎨 Generating image, please wait...")

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512
    }

    try:
        response = requests.post(SD_API_URL, json=payload)
        response.raise_for_status()
        image_data = response.json()["images"][0]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image_file = BytesIO(image_bytes)
        image_file.name = "generated.png"

        await update.message.reply_photo(photo=image_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Error generating image: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    app.run_polling()

if __name__ == "__main__":
    main()

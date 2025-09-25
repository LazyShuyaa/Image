import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from diffusers import StableDiffusionPipeline
import torch

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8203565510:AAGZxqRrZzu8boqqVZZG21jmkyfQ4v3xNdc")

# Load base model from Hugging Face
print("🔄 Loading base model config...")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    safety_checker=None
)

# Override weights with your local .safetensors file
print("🔄 Loading local weights...")
pipe.load_checkpoint("/root/Image/model.safetensors")
pipe.to("cuda" if torch.cuda.is_available() else "cpu")
print("✅ Model ready!")

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a prompt and I'll generate an image!")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("🎨 Generating image, please wait...")
    image = pipe(prompt).images[0]
    image.save("output.png")
    await update.message.reply_photo(photo=open("output.png", "rb"))

# Bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

# Run the bot
app.run_polling()

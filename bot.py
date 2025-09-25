
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from diffusers import StableDiffusionPipeline
import torch

# Load the full model from local .safetensors file
print("🔄 Loading model...")
pipe = StableDiffusionPipeline.from_ckpt(
    "model.safetensors", torch_dtype=torch.float16
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")
print("✅ Model loaded and ready!")

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
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

# Run the bot
app.run_polling()

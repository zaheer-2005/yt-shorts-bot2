from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

TOKEN = "7846447392:AAFNDQ2bsSVq6ivib3ZK74JGV6GKr9Ou_NM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube Shorts link to download!")

async def download_shorts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com/shorts/" not in url:
        await update.message.reply_text("❌ Invalid URL. Please send a YouTube Shorts link.")
        return

    await update.message.reply_text("📥 Downloading...")

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'shorts.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open("shorts.mp4", "rb"))
        os.remove("shorts.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_shorts))
app.run_polling()

import os
import yt_dlp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8483787111:AAFzc65rX_78C3DugnefCaYUDsG95FGNr-c"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a YouTube link and I will download the video."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send a valid YouTube link.")
        return

    await update.message.reply_text("Downloading video...")

    try:
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_text("Uploading video...")

        with open(filename, "rb") as video_file:
            await update.message.reply_video(video=video_file)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
)

print("Bot is running...")
app.run_polling()
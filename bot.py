import os
import time
import asyncio
from pathlib import Path
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
COOKIES_FILE = Path(os.environ.get("YTDLP_COOKIES_FILE", "cookies.txt"))
COOKIES_FROM_BROWSER = os.environ.get("YTDLP_COOKIES_FROM_BROWSER")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a YouTube link and I will download the video."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send a valid YouTube link.")
        return

    status_message = await update.message.reply_text("Downloading: 0%")
    chat_id = update.effective_chat.id
    message_id = status_message.message_id

    try:
        last = {"percent": -1, "time": 0}

        def progress_hook(d):
            try:
                if d.get("status") == "downloading":
                    downloaded = d.get("downloaded_bytes") or 0
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    if total:
                        percent = int(downloaded * 100 / total)
                    else:
                        percent = None
                    now = time.time()
                    # throttle: update when percent increases by >=2 or every 5s
                    if percent is not None and (percent - last["percent"] >= 2 or now - last["time"] > 5):
                        last["percent"] = percent
                        last["time"] = now
                        text = f"Downloading: {percent}%"
                        try:
                            asyncio.get_event_loop().create_task(
                                context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
                            )
                        except Exception:
                            pass
            except Exception:
                pass

        ydl_opts = {
            "format": "18",
            "outtmpl": "video.mp4",
            "progress_hooks": [progress_hook],
        }

        if COOKIES_FROM_BROWSER:
            ydl_opts["cookies_from_browser"] = COOKIES_FROM_BROWSER
        elif COOKIES_FILE.exists():
            ydl_opts["cookiefile"] = str(COOKIES_FILE)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # ensure final 100% update
        try:
            asyncio.get_event_loop().create_task(
                context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Downloading: 100%")
            )
        except Exception:
            pass

        await update.message.reply_text("Uploading video...")

        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video=video)

        os.remove("video.mp4")

    except Exception as e:
        error_text = str(e)
        if "Sign in to confirm" in error_text or "bot" in error_text and "cookies" in error_text.lower():
            await update.message.reply_text(
                "This video needs YouTube cookies or browser auth. "
                "Add a cookies.txt file in the bot folder or set YTDLP_COOKIES_FILE, "
                "or set YTDLP_COOKIES_FROM_BROWSER to your browser name."
            )
        else:
            await update.message.reply_text(f"Error: {error_text}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
)

print("Bot is running...")
app.run_polling()

import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- WEB SERVER FOR RENDER ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Insta MP3 Bot is Alive!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# -----------------------------

TOKEN = "8671935397:AAH1EP3e3rJwgzpGj3D-wUhZ6NVigSalHdQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me an Instagram Reel link to get MP3.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Send only Instagram links.")
        return

    wait_msg = await update.message.reply_text("⏳ Processing Instagram Reel...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
        
        await update.message.reply_audio(audio=open(file_path, 'rb'))
        await wait_msg.delete()
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
    

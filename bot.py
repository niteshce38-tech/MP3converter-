import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- WEB SERVER FOR RENDER (Keep Alive) ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "Techverse Bot is Running!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# ------------------------------------------

TOKEN = "8671935397:AAH1EP3e3rJwgzpGj3D-wUhZ6NVigSalHdQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 **Techverse Insta-MP3 Bot** ready hai!\n\nBas Instagram Reel ka link bhejo aur MP3 pao.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Bhai, sirf Instagram link bhejo.")
        return

    wait_msg = await update.message.reply_text("⏳ Processing with Cookies... (Wait karo)")

    # COOKIES WALI SETTINGS
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        'cookiefile': 'instagram.com_cookies.txt', # <--- Laptop se upload ki hui file
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'add_header': [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_name = ydl.prepare_filename(info)
            file_path = os.path.splitext(temp_name)[0] + ".mp3"
        
        await update.message.reply_audio(
            audio=open(file_path, 'rb'), 
            caption="Downloaded by @Techverse"
        )
        await wait_msg.delete()
        os.remove(file_path)

    except Exception as e:
        await wait_msg.delete()
        await update.message.reply_text(f"❌ Error: Cookies expire ho gayi hain ya file missing hai.\n\nDetail: {str(e)[:100]}")

if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🚀 Bot starting with Cookie support...")
    app.run_polling()
    

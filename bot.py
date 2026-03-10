import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- WEB SERVER FOR RENDER (Keep Alive) ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Insta MP3 Bot is Alive!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# ------------------------------------------

TOKEN = "8671935397:AAH1EP3e3rJwgzpGj3D-wUhZ6NVigSalHdQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Welcome to The Insta-MP3 Converter!**\n\n"
        "Mujhe kisi bhi Instagram Reel ka link bhejo, main uska audio (MP3) nikaal kar bhej dunga.\n\n"
        "⚠️ **Note:** Private accounts ke video download nahi honge.",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    # Check if it's an Instagram link
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Bhai, ye Instagram ka link nahi hai. Sirf Insta Reels/Videos bhejo.")
        return

    wait_msg = await update.message.reply_text("⏳ Instagram se audio nikaal raha hoon... Sabar rakho.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{chat_id}_%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        # Instagram bypass headers
        'add_header': [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
    }

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_name = ydl.prepare_filename(info)
            file_path = os.path.splitext(temp_name)[0] + ".mp3"
        
        # Audio send karna
        await update.message.reply_audio(
            audio=open(file_path, 'rb'), 
            title=info.get('title', 'Insta Audio')
        )
        await wait_msg.delete()
        
        # Cleanup
        os.remove(file_path)

    except Exception as e:
        await wait_msg.delete()
        error_msg = str(e)
        if "login" in error_msg.lower():
            await update.message.reply_text("❌ Ye account Private hai. Main sirf Public reels download kar sakta hoon.")
        else:
            await update.message.reply_text(f"❌ Kuch gadbad hui: {error_msg[:100]}")

if __name__ == '__main__':
    keep_alive() 
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Techverse Insta Bot Running...")
    app.run_polling()
        ]
    }

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # File ka naam handle karna
            temp_name = ydl.prepare_filename(info)
            # Extension change handle karna (webm/m4a to mp3)
            file_path = os.path.splitext(temp_name)[0] + ".mp3"
        
        # Audio send karna
        await update.message.reply_audio(
            audio=open(file_path, 'rb'), 
            title=info.get('title', 'Converted Audio')
        )
        await wait_msg.delete()
        
        # Safai abhiyaan (Delete file)
        os.remove(file_path)

    except Exception as e:
        error_text = str(e)
        if "login" in error_text.lower():
            await update.message.reply_text("❌ Error: Ye Instagram account Private hai. Sirf Public links bhejo.")
        else:
            await update.message.reply_text(f"❌ Kuch gadbad hui: {error_text[:100]}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🚀 All-in-One Bot is running...")
    app.run_polling()
    

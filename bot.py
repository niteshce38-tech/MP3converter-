import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Tumhara Token
TOKEN = "8671935397:AAH1EP3e3rJwgzpGj3D-wUhZ6NVigSalHdQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Balle Balle! Main YouTube aur Instagram dono ke liye ready hoon.\n\nBas link bhejo aur MP3 pao!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    # Check if it's a link
    if not url.startswith("http"):
        await update.message.reply_text("Bhai, ye link nahi hai. Sahi link bhejo!")
        return

    wait_msg = await update.message.reply_text("⏳ Wait... Main video se audio nikaal raha hoon (Insta/YouTube dono chalenge).")

    # Sabse important settings
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{chat_id}_%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Kuch extra settings Insta ke liye
        'quiet': True,
        'no_warnings': True,
        'add_header': [
            'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
    

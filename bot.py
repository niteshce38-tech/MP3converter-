import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8671935397:AAH1EP3e3rJwgzpGj3D-wUhZ6NVigSalHdQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bhai link bhejo, main MP3 bana ke deta hoon! 🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Sirf YouTube link bhejo bhai.")
        return

    wait_msg = await update.message.reply_text("⏳ Wait karo... MP3 nikaal raha hoon.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
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
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
  

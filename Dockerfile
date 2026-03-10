FROM python:3.10-slim

# FFmpeg install karne ke liye
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . .

# Is line se requirements.txt ki saari libraries install hongi
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]

FROM python:3.9-slim

# ffmpegをインストール（動画処理に必要）
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# main.pyを実行
CMD ["python", "main.py"]

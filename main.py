import os
import uuid
import glob
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = 'static/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    # 掃除
    for f in glob.glob(f'{DOWNLOAD_FOLDER}/*.mp4'):
        try: os.remove(f)
        except: pass

    unique_id = str(uuid.uuid4())
    filepath = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp4")

    ydl_opts = {
        'format': 'best[height<=720][ext=mp4]/best',
        'outtmpl': filepath,
        'nocheckcertificate': True,
        'quiet': True,
        # KoyebのIPが弾かれた時用の悪あがき設定
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return jsonify({
                'success': True,
                'file_path': f'/static/downloads/{unique_id}.mp4',
                'file_name': f"{info.get('title', 'video')}.mp4"
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Koyebは環境変数PORTを割り当てるのでそれに合わせる
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

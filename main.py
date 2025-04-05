from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
from io import BytesIO

app = Flask(__name__)
CORS(app)

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return filename, info

@app.route('/download', methods=['POST'])
def handle_download():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        filename, info = download_audio(url)
        
        with open(filename, 'rb') as f:
            audio_blob = BytesIO(f.read())
        
        os.remove(filename)
        
        return send_file(
            audio_blob,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=f"{info['title']}.mp3",
            etag=False
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host='0.0.0.0', port=port)  # Critical for Render
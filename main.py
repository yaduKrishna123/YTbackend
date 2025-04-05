# import yt_dlp

# def get_audio_only(url):
#     # Specify options to download only audio with the best quality
#     ydl_opts = {
#         'format': 'bestaudio',  # Use only audio with the best quality
#         'extractaudio': True,  # Extract audio only
#         'audioquality': 0,  # Best audio quality
#         'outtmpl': '%(title)s.%(ext)s',  # Output filename template (video title as filename)
#         'quiet': True,  # Suppress unnecessary output
#         'noplaylist': True,  # Don't download entire playlists if URL points to one
#         'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Path to FFmpeg binary (if necessary)
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',  # Correct postprocessor key
#             'preferredcodec': 'mp3',  # Convert to mp3
#             'preferredquality': '0',  # Highest audio quality
#         }]
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # Download the audio and get information
#         result = ydl.extract_info(url, download=True)
#         print(f"Title: {result['title']}")
#         print(f"Uploader: {result['uploader']}")
#         print(f"Audio Format: {result['formats'][0]['ext']}")  # Show the audio format (e.g., mp3, webm)
#         print("Audio downloaded")

# # Example usage
# video_url = 'https://youtu.be/5yb2N3pnztU?si=PEURBupVjnRfIFO-'  # Replace with your video URL
# get_audio_only(video_url)


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Add this import
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
        
        # Read the file into memory as bytes
        with open(filename, 'rb') as f:
            audio_blob = BytesIO(f.read())
        
        # Clean up the file
        os.remove(filename)
        
        # Send as blob with metadata
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
    app.run(port=5000, debug=True)
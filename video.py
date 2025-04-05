import yt_dlp

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Do not download the actual video, just extract metadata
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        print(f"Title: {result['title']}")
        print(f"Uploader: {result['uploader']}")
        print(f"Duration: {result['duration']} seconds")
        print(f"Views: {result['view_count']}")
        print(f"Description: {result['description']}")

# Example usage
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
get_video_info(video_url)

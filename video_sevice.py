import yt_dlp
import os
import datetime

def genrateUniqueName():

    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")



def download_youtube_video(url):
    file_name=genrateUniqueName()
    os.makedirs('audio_youtube', exist_ok=True)
    yt_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': f'audio_youtube/{file_name}.%(ext)s',
    'merge_output_format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',

    }],
    'exec_cmd': 'ffmpeg -ss 2 -i {} -t 5 -c copy "{}"',
    'progress_hooks': [lambda d: print(f"\r{d.get('status', 'Downloading')} ({(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)):.2%})", end='')]
    }


    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])

    return 'audio_youtube/'+file_name+'.mp3'




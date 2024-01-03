from moviepy.editor import VideoFileClip
import numpy as np
import os
import subprocess
from datetime import datetime
import ffmpeg
import io
import yt_dlp
import os
import datetime
import numpy as np

from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import io

#def download_audio_from_youtube(youtube_url):
    # Create a YouTube object
#    yt = YouTube(youtube_url)

    # Select the audio stream (you may want to choose the best quality)
#    audio_stream = yt.streams.filter(only_audio=True).first()

#    audio_buffer = io.BytesIO()
#    audio_stream.stream_to_buffer(audio_buffer)

    # Set the buffer position to the beginning
#    audio_buffer.seek(0)

    # Convert the audio bytes to a NumPy array
#    audio_array = np.frombuffer(audio_buffer.read(), dtype=np.int16)

#    print('video Downlaoaded successfully')
#    return audio_buffer.read()
def download_audio_from_youtube(youtube_url):
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Select the audio stream (you may want to choose the best quality)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Define the path where you want to save the audio file in your Colab environment
    save_path = 'output_audio/audio.mp3'  # Change the filename and extension if you prefer a different format

    # Get the actual file name downloaded by pytube
    actual_file_name = audio_stream.default_filename
    audio_stream.download(output_path='output_audio', filename='audio.mp3')

    # Rename the downloaded file to your preferred name
    # os.rename(os.path.join('', actual_file_name), save_path)
    print("video Download Successfully")
    return save_path


def genrateUniqueName():
    
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    


def download_youtube_video(url):
    file_name=genrateUniqueName()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    os.makedirs('audio_youtube', exist_ok=True)
    yt_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': f'audio_youtube/{file_name}.%(ext)s',
#    'merge_output_format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
	'nopostoverwrites': True,  # Do not overwrite files if they already exist

       
    }],
    'exec_cmd': 'ffmpeg -ss 2 -i {} -t 5 -c copy "{}"',
    'progress_hooks': [lambda d: print(f"\r{d.get('status', 'Downloading')} ({(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)):.2%})", end='')],
    'headers': headers,
    }


    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])

    return 'audio_youtube/'+file_name+'.mp3'


#def convert_video_to_audio(input_video, output_audio):
#    command = [
#        'ffmpeg',
#        '-i', input_video,
#        '-vn',
#        '-acodec', 'pcm_s16le',
#        '-ar', '44100',
#        '-ac', '2',
#        output_audio
#    ]
#
#    try:
#        subprocess.run(command, check=True)
#        print(f"Conversion successful. Audio saved as {output_audio}")
#	return output_path
#    except subprocess.CalledProcessError as e:
#        print(f"Error during conversion: {e}")

def convert_video_to_audio(video_path):
    os.makedirs('video_to_audio', exist_ok=True)
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Extract the audio from the video
    audio_clip = video_clip.audio


    id=genrateUniqueName()

    output_path=f"audio/{id}"+video_path.split('.')[0]+".mp3"

    # Save the audio to a new file
    audio_clip.write_audiofile(output_path)

    video_clip.close()
    audio_clip.close()

    return output_path



#def get_mono_waveform(input_path):
   # audio = AudioSegment.from_file(input_path)
    
    # Ensure mono audio
  #  audio = audio.set_channels(1)
    
    # Extract raw audio data as NumPy array
 #   samples = np.array(audio.get_array_of_samples())
    
#    return samples

def convertVideo(video_file_path):
    """
    This function converts a video file into an audio file.

    Parameters:
    video_file_path (str): The file path of the video file to convert.
    """
    try:
        # Run FFmpeg command to convert video to audio and store the result in a variable
        command = [
            'ffmpeg',
            '-i', video_file_path,
            '-f', 'wav',  # Change to 'mp3' or other audio format if needed
            '-ac', '2',   # Number of audio channels
            '-ar', '44100',  # Audio sample rate
            '-acodec', 'pcm_s16le',  # Audio codec
            '-vn', '-loglevel', 'quiet',  # Disable video and set log level to quiet
            '-'
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error {type(e).__name__} occurred: {e}")
        return None

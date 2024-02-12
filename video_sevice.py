from moviepy.editor import VideoFileClip
import numpy as np
import os
import subprocess
import ffmpeg
import io
import os
import datetime
import numpy as np
from pydub import AudioSegment
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import io

def genrateUniqueName():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


def download_audio_from_youtube(youtube_url):
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Select the audio stream (you may want to choose the best quality)
    audio_stream = yt.streams.filter(only_audio=True).first()
    id=genrateUniqueName()
    print(id)
    # Define the path where you want to save the audio file in your Colab environment
    save_path = f'{id}output_audio/audio.mp3'  # Change the filename and extension if you prefer a different format

    # Get the actual file name downloaded by pytube
    actual_file_name = audio_stream.default_filename
    audio_stream.download(output_path=f'{id}output_audio', filename='audio.mp3')

    # Rename the downloaded file to your preferred name
    # os.rename(os.path.join('', actual_file_name), save_path)
    print("Youtube Video was Downloaded Successfully")
    return save_path


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


def convertVideo(input_video_path):
    format = "mp3"
    # Extract the base name of the input video file
    base_name = os.path.basename(input_video_path)
    # Remove the file extension to get the name without the extension
    file_name, _ = os.path.splitext(base_name)
    # Create the output audio file path with the same name as the input video
    id = genrateUniqueName()
    audio_file_path = f"{id}_{file_name}_audio.{format}"
    audio = AudioSegment.from_file(input_video_path)
    audio.export(audio_file_path, format=format)
    return audio_file_path
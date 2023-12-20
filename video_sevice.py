from pytube import YouTube
from moviepy.editor import VideoFileClip
import os


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

    return save_path


def convertVideo(video_file_path):
    """
    This function converts a video file into an audio file.

    Parameters:
    video_file_path (str): The file path of the video file to convert.
    """
    # Load the video file
    video = VideoFileClip(video_file_path)

    # Extract the audio from the video
    audio = video.audio
    audio_file_path = f"outputAudio/{video.filename}"
    # Write the audio to a file
    audio.write_audiofile(audio_file_path)

    # Close the video and audio files to free up resources
    audio.close()
    video.close()
    return audio.filename
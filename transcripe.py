
from video_sevice import download_youtube_video
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import numpy as np
import whisper
from video_sevice import genrateUniqueName


model= whisper.load_model('large-v3',download_root='whisper_model')

def is_human_speech(chunk, amplitude_threshold=-30):
    # Convert the audio chunk to a numpy array
    audio_array = np.array(chunk.get_array_of_samples())

    # Calculate the amplitude of the audio chunk
    amplitude = np.mean(np.abs(audio_array))

    # Check if the amplitude is above the threshold
    return amplitude > amplitude_threshold



def transcribe_whisper(input_file, silence_threshold=-40, min_silence_duration=1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    output_folder="output_audio_chuncks"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Split the audio based on silence
    chunks = split_on_silence(audio, silence_thresh=silence_threshold, min_silence_len=min_silence_duration)
    human_speech_chunks = [chunk for chunk in chunks if is_human_speech(chunk)]

    id=genrateUniqueName()


    text = ""
    # Save each chunk to the output folder
    for i, chunk in enumerate(human_speech_chunks):
        output_file = os.path.join(output_folder, f"chunk_{str(id)}_{str(i)}.wav")
        chunk.export(output_file, format="wav")
        text += model.transcribe(output_file)['text']
        # print(f"chunk_{i}")
        # print(text)
    
        # Remove the output folder after processing
        # os.remove(output_file)
    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error while deleting {file_path}: {e}")
      
    return str(text)


def transcribeLink(link):
  audio=download_youtube_video(link)
  res=transcribe_whisper(audio)
#   os.remove(audio)
  for file_name in os.listdir("audio_youtube"):
        file_path = os.path.join("audio_youtube", file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error while deleting {file_path}: {e}")
#   print(res)
  return res


def transcribeVideo(video_path):
    result = transcribe_whisper(video_path)
    return result 


def transcribeAudio(audio_path):
    result = transcribe_whisper(audio_path)
    return result



    







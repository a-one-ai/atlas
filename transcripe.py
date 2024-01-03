import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from video_sevice import convertVideo , download_audio_from_youtube
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
import datetime
import concurrent.futures
# Load model and processor offline
model_directory = "./models"

model = AutoModelForSpeechSeq2Seq.from_pretrained(model_directory)
processor = AutoProcessor.from_pretrained(model_directory)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32




pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=150,
    chunk_length_s=20,
    batch_size=18,
    return_timestamps=False,
#    torch_dtype=torch_dtype,
    device=device,
   
)

def genrateUniqueName():

    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

def transcribe(audio):
    res=pipe(audio)['text']
    return res

def split_audio(input_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)


    output_folder='audio_chuncks'
    # Get the duration of the audio in seconds
    audio_duration = len(audio) / 1000  # in seconds
    chunk_duration= 800

    # Calculate the number of chunks
    num_chunks = int(audio_duration / chunk_duration)+1

    pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=140,
    chunk_length_s=20,
    batch_size=18,
    return_timestamps=True,
#    torch_dtype=torch_dtype,
    device=device,
    )

    text=""
    chunk_paths=[]
    transcriptions = []

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Split the audio into chunks
    for i in range(num_chunks):
        start_time = i * chunk_duration * 1000  # convert to milliseconds
        end_time = (i + 1) * chunk_duration * 1000  # convert to milliseconds
        chunk = audio[start_time:end_time]
        if(end_time>(audio_duration*1000)):

          chunk = audio[start_time:(audio_duration*1000)]

        #chunk_path = os.path.join(output_folder, f"chunk_{i + 1}.wav")
        #chunk.export(chunk_path, format="wav")
        #chunk_paths.append(chunk_path)
        # Save each chunk to the output folder
        chunk.export(os.path.join(output_folder, f"chunk_{i + 1}.wav"), format="wav")
        text+=pipe(f"{output_folder}/chunk_{i + 1}.wav")['text']

#    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use list comprehension to collect results
#        transcriptions = list(executor.map(transcribe, chunk_paths))
    for chunk_path in chunk_paths:
      os.remove(chunk_path)
      
#    for element in transcriptions:
#      text += element
    return text

def transcribe_whisper(audio_file):

    audio = AudioSegment.from_file(audio_file)

    # Get the duration of the audio in seconds
    audio_duration = len(audio) / 1000
    if(audio_duration>900):
      res=split_audio(audio_file)
      return res
    else:
       res=pipe(audio_file)['text']
       return res

def transcribeLink(link):
    audio=download_audio_from_youtube(link)
    result=transcribe_whisper(audio)
#  result=pipe(audio)['text']
    if os.path.exists(audio):
      os.remove(audio)
    return result

def transcribeVideo(video_path):
   audio=convertVideo(video_path)
   result=transcribe_whisper(audio)
#  result=pipe(audio)['text']
#  result=pipe(video_path)['text']
   if os.path.exists(audio):
     os.remove(audio)
   return result

def transcribeAudio(audio_path):

   result=transcribe_whisper(audio_path)
#   result=pipe(audio_path)['text']
   return result







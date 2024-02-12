import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from video_sevice import convertVideo , download_audio_from_youtube
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
import datetime
import concurrent.futures
import shutil
import time


# Check CUDA availability
device = torch.device("cuda:0")
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
# Load model and processor offline
model_id = r"U:\\ALL PROJECTS __IMPORTANT__\\atlas\\model"
#model_id = "openai/whisper-medium"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, local_files_only = True
)


model.to(device)
processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
    generate_kwargs={"task": "transcribe"},
)


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been successfully deleted.")
    except Exception as e:
        print(f"An error occurred while deleting the folder '{folder_path}': {e}")


def genrateUniqueName():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


def transcribe(audio):
    res=pipe(audio)['text']
    return res


def split_audio(input_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file[0])


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
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
        generate_kwargs={"task": "transcribe"},
    )

    text=""
    chunk_paths=[]

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

        chunk.export(os.path.join(output_folder, f"chunk_{i + 1}.wav"), format="wav")
        text+=pipe(f"{output_folder}/chunk_{i + 1}.wav",return_timestamps='True')['text']

    delete_folder(input_file)

    return text

def transcribe_whisper(audio_file):
    start = time.time()

    audio = AudioSegment.from_file(str(audio_file))

    # Get the duration of the audio in seconds
    audio_duration = len(audio) / 1000
    if(audio_duration>900):

        res=split_audio(audio_file)
        delete_folder(audio_file[:20]+"output_audio")
        end = time.time()
        print(float(end - start))
        return res
    
    else:
        
        res=pipe(audio_file)['text']
        delete_folder(audio_file)
        end = time.time()
        print(float(end - start))
        return res


def transcribeLink(link):

    audio=download_audio_from_youtube(link)
    result=transcribe_whisper(audio)
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

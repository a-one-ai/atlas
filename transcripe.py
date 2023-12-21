import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from video_sevice import download_audio_from_youtube, convertVideo

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=60,
    batch_size=16,
    return_timestamps=False,
    torch_dtype=torch_dtype,
    device=device,
)


def transcribeLink(link):
    audio = download_audio_from_youtube(link)
    audio1 = AudioSegment.from_file(audio)
    result = pipe(audio1)
    return result['text']


def transcribeVideo(video_path):
    audio = convertVideo(video_path)
    result = pipe(audio)
    return result['text']


def transcribeAudio(audio_path):
    result = pipe(audio_path)
    return result['text']


def translate_en_script(input, script_lang):
    if script_lang == 'en':
        return input
    







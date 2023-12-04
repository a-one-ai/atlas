"""# Import_library"""
import whisper
from pytube import YouTube
from whisper.utils import format_timestamp
from summa.summarizer import summarize
from deep_translator import GoogleTranslator
from langdetect import detect
model = whisper.load_model("large-v3")

"""# All_Funcation"""

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


def Transcribe_whisper(audio_path):
# Transcribe the audio from the video
  text_time = model.transcribe(audio_path)
  script=text_time['text']
  script_time=[]
  script_lang=text_time['language']

  #with open("transcription_with_timestamps.txt", "w", encoding="utf-8") as output_file:
  for segment in text_time['segments']:
      start, end, text = segment["start"], segment["end"], segment["text"]
      line = f"[{format_timestamp(start)} - {format_timestamp(end)}]  {text}"
      #output_file.write(line + "\n")
      script_time.append(line)

  return script,script_lang,script_time

def translate_en_script(input,script_lang):
  if(script_lang=='en'):
      return input

  else:
    max_chunk_length = 500  # The maximum allowed query length
    text_chunks = [
        input[i : i + max_chunk_length] for i in range(0, len(input), max_chunk_length)
        ]
    translated_chunks = [GoogleTranslator(source='auto', target='en').translate(chunk) for chunk in text_chunks]
    translated_text = " ".join(translated_chunks)
    return translated_text

def translate_ar_script(input,script_lang):
  if(script_lang=='ar'):
      return input

  else:
    max_chunk_length = 500  # The maximum allowed query length
    text_chunks = [
        input[i : i + max_chunk_length] for i in range(0, len(input), max_chunk_length)
        ]
    translated_chunks = [GoogleTranslator(source='auto', target='ar').translate(chunk) for chunk in text_chunks]
    translated_text = " ".join(translated_chunks)
    return translated_text


def translate_en(input):

        max_chunk_length = 500  # The maximum allowed query length
        text_chunks = [
          input[i : i + max_chunk_length] for i in range(0, len(input), max_chunk_length)
          ]
        translated_chunks = [GoogleTranslator(source='auto', target='en').translate(chunk) for chunk in text_chunks]
        translated_text = " ".join(translated_chunks)
        return translated_text

def translate_ar(input):

        max_chunk_length = 500  # The maximum allowed query length
        text_chunks = [
          input[i : i + max_chunk_length] for i in range(0, len(input), max_chunk_length)
          ]
        translated_chunks = [GoogleTranslator(source='auto', target='ar').translate(chunk) for chunk in text_chunks]
        translated_text = " ".join(translated_chunks)
        return translated_text

def get_summary(text):
    en_summary = summarize(text,ratio=0.2, language="english")
    ar_summary=translate_ar(en_summary)

    return en_summary,ar_summary

"""# Finial_recall_funcation"""

def proccesVideoAudioFile(video_audio_File_Path):
  print(f" 2video file path {video_audio_File_Path}")
  script,script_lang,script_time=Transcribe_whisper(video_audio_File_Path)
  ar_script=translate_ar_script(script,script_lang)
  en_script=translate_en_script(script,script_lang)
  en_summary,ar_summary=get_summary(en_script)

  result={
      "ar_script":ar_script,
      "en_script":en_script,
      "ar_summary":ar_summary,
      "en_summary":en_summary,
      "script_time":script_time,
  }

  return result

# video_link="/content/أبو عبيدة تمكنا من تدمير 20 آلية عسكرية إسرائيلية خلال الـ48 ساعة تدميرا كليا أو جزئيا.mp4"
# print(proccesVideoAudioFile(video_link))

def proccesYoutubeLinkVideo(link):
  audio_path=download_audio_from_youtube(link)
  script,script_lang,script_time=Transcribe_whisper(audio_path)
  ar_script=translate_ar_script(script,script_lang)
  en_script=translate_en_script(script,script_lang)
  en_summary,ar_summary=get_summary(en_script)

  result={
      "ar_script":ar_script,
      "en_script":en_script,
      "ar_summary":ar_summary,
      "en_summary":en_summary,
      "script_time":script_time,
  }

  return result

# link="https://youtu.be/WkZfDvnNyAo?si=fyDhHyrfBfriEls7"
# print(proccesYoutubeLinkVideo(link))
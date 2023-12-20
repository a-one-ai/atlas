"""# Import_library"""

from summa.summarizer import summarize
from deep_translator import GoogleTranslator
from langdetect import detect
from video_sevice import download_audio_from_youtube,convertVideo
from transcripe import pipe


"""# All_Funcation"""

def transcribeLink(link):
  audio=download_audio_from_youtube(link)
  result=pipe(audio)
  return result['text']

def trnascribeVideo(video_path):
  audio=convertVideo(video_path)
  result=pipe(audio)
  return result['text']

def transcribeAudio(audio_path):
   result=pipe(audio_path)
   return result['text']

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

def proccesVideoAudioFile(video_file_path):
  script=trnascribeVideo(video_file_path)
  ar_script=translate_ar(script)
  en_script=translate_en(script)
  en_summary,ar_summary=get_summary(en_script)

  result={
      "ar_script":ar_script,
      "en_script":en_script,
      "ar_summary":ar_summary,
      "en_summary":en_summary,
      
  }

  return result

def proccesAudioFile(audio_File_Path):
  script=transcribeAudio(audio_File_Path)
  ar_script=translate_ar(script)
  en_script=translate_en(script)
  en_summary,ar_summary=get_summary(en_script)

  result={
      "ar_script":ar_script,
      "en_script":en_script,
      "ar_summary":ar_summary,
      "en_summary":en_summary,

  }

  return result

# video_link="/content/أبو عبيدة تمكنا من تدمير 20 آلية عسكرية إسرائيلية خلال الـ48 ساعة تدميرا كليا أو جزئيا.mp4"
# print(proccesVideoAudioFile(video_link))

def proccesYoutubeLinkVideo(link):
 
  script=transcribeLink(link)
  ar_script=translate_ar(script)
  en_script=translate_en(script)
  en_summary,ar_summary=get_summary(en_script)

  result={
      "ar_script":ar_script,
      "en_script":en_script,
      "ar_summary":ar_summary,
      "en_summary":en_summary,
  }

  return result

# link="https://youtu.be/WkZfDvnNyAo?si=fyDhHyrfBfriEls7"
# print(proccesYoutubeLinkVideo(link))
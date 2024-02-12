"""# Import_library"""

from deep_translator import GoogleTranslator
from langdetect import detect
from transcripe import transcribeAudio,transcribeLink,transcribeVideo
import os

"""# All_Funcation"""

def translate_en_script(input,script_lang):
    max_chunk_length = 500  # The maximum allowed query length
    text_chunks = [
        input[i : i + max_chunk_length] for i in range(0, len(input), max_chunk_length)
        ]
    translated_chunks = [GoogleTranslator(source='auto', target='en').translate(chunk) for chunk in text_chunks]
    translated_text = " ".join(translated_chunks)
    return translated_text

def translate_ar_script(input,script_lang):
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


"""# Finial_recall_funcation"""

def proccesVideoFile(video_file_path):
  script=transcribeVideo(video_file_path)

  result={
      "ar_script":"",
      "en_script":"",
      "ar_summary":"",
      "en_summary":"",
      "script":script	
  }

  return result

def proccesAudioFile(audio_File_Path):
  script=transcribeAudio(audio_File_Path)

  result={
      "ar_script":"",
      "en_script":"",
      "ar_summary":"",
      "en_summary":"",
      "script":script   
  }

  return result

# video_link="/content/أبو عبيدة تمكنا من تدمير 20 آلية عسكرية إسرائيلية خلال الـ48 ساعة تدميرا كليا أو جزئيا.mp4"
# print(proccesVideoAudioFile(video_link))

def proccesYoutubeLinkVideo(link, tr = "False"):
  print(tr)
  script=transcribeLink(link)

  if tr != "False":
      result={
          "translation":translate_ar(script),
          "script":script   
      }
  else:
      result={
      "translation":"",
      "script":script   
  }

  return result



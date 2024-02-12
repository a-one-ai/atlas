import base64
import sys
import requests
import datetime
import re
from transcripe import transcribe_whisper
import os 

def create_onedrive_directdownload (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl


def genrateUniqueName():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

def download_file_from_onedrive(file_id, destination):
    URL = create_onedrive_directdownload(file_id)
    print(URL)

    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def onedrive_downloader(link):
    try:
        id = genrateUniqueName()
        destination = f"./downloaders/downloads/drive-{id}.mp4"

        print(f"dowload {link} to {destination}")
        download_file_from_onedrive(link, destination)
        res = transcribe_whisper(destination)
        os.remove(destination)
        return res
    except Exception as e:
        return e

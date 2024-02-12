import sys
import requests
import datetime
import re

def genrateUniqueName():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

def download_file_from_google_drive(file_id, destination):
    URL = re.sub(r"https://drive\.google\.com/file/d/(.*?)/.*?\?usp=sharing", r"https://drive.google.com/uc?export=download&id=\1", file_id )

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


def drive_downloader(link):
    try:
        id = genrateUniqueName()
        destination = f"./downloaders/downloads/drive-{id}.mp4"

        print(f"dowload {link} to {destination}")
        download_file_from_google_drive(link, destination)

        return destination
    except Exception as e:
        return e

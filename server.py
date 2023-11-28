from flask import Flask, render_template, jsonify, request
from models import processVideoAudioFile, processYoutubeLinkVideo
import os

app = Flask(__name__)

# Configuration
UPLOAD_VIDEOS_FOLDER = "./uploaded_videos"
UPLOAD_AUDIOS_FOLDER = "./uploaded_audios"
PORT = 8000

# Create necessary directories
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

create_directory(UPLOAD_VIDEOS_FOLDER)
create_directory(UPLOAD_AUDIOS_FOLDER)

@app.route("/", methods=["GET"])
def index():
    """Render the index page."""
    return render_template("index.html")

def process_file(file, folder_path, process_function):
    """Generic file processing function."""
    try:
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)
        result = process_function(file_path)
        return jsonify({"data": result})
    except Exception as e:
        print(f"Error {type(e)} occurred: {e}")
        return jsonify({"data": "Error processing file. Please try again."})

@app.route("/getAudioFile", methods=["POST"])
def process_audio():
    """Process uploaded audio files."""
    audio = request.files.get("audio")
    if audio and audio.filename:
        return process_file(audio, UPLOAD_AUDIOS_FOLDER, processVideoAudioFile)
    return jsonify({"data": "Invalid audio file. Please upload a valid file."})

@app.route("/getVideoFile", methods=["POST"])
def process_video():
    """Process uploaded video files."""
    video = request.files.get("video")
    if video and video.filename:
        return process_file(video, UPLOAD_VIDEOS_FOLDER, processVideoAudioFile)
    return jsonify({"data": "Invalid video file. Please upload a valid file."})

@app.route("/getYoutubeVideoLink", methods=["POST"])
def process_youtube_link():
    """Process YouTube video links."""
    video_link = request.form.get("youtubeVideoLink", request.json.get("link"))
    if video_link:
        try:
            result = processYoutubeLinkVideo(video_link)
            return jsonify({"data": result})
        except Exception as e:
            print(f"Error {type(e)} occurred: {e}")
            return jsonify({"data": "Error processing YouTube link. Please try again."})
    return jsonify({"data": "Please provide a YouTube video link."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=PORT)

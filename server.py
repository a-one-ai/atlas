from flask import Flask, render_template, jsonify, request
from models import proccesVideoAudioFile, proccesYoutubeLinkVideo
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        print(f"Error {type(e).__name__} occurred: {e}")
        return jsonify({"error": "Internal server error. File processing failed."}), 500

@app.route("/getAudioFile", methods=["POST"])
def process_audio():
    """Process uploaded audio files."""
    audio = request.files.get("audio")
    print(type(audio))
    if audio and audio.filename:
        return process_file(audio, UPLOAD_AUDIOS_FOLDER, proccesVideoAudioFile)
    return jsonify({"error": "Invalid audio file. Please upload a valid file."}), 400

@app.route("/getVideoFile", methods=["POST"])
def process_video():
    """Process uploaded video files."""
    video = request.files.get("video")
    if video and video.filename:
        return process_file(video, UPLOAD_VIDEOS_FOLDER, proccesVideoAudioFile)
    return jsonify({"error": "Invalid video file. Please upload a valid file."}), 400

@app.route("/getYoutubeVideoLink", methods=["POST"])
def process_youtube_link():
    """Process YouTube video links."""

    # Try to get the link from form data
    video_link = request.form.get("link")

    # If not in form data, try to get it from JSON body
    if not video_link:
        json_data = request.get_json()
        if json_data and "link" in json_data:
            video_link = json_data["link"]

    # Check if the link is received
    if video_link:
        try:
            result = proccesYoutubeLinkVideo(video_link)
            return jsonify({"data": result})
        except Exception as e:
            print(f"Error {type(e).__name__} occurred: {e}")
            return jsonify({"error": "Internal server error. YouTube link processing failed."}), 500

    # If no link is provided in either form or JSON
    return jsonify({"error": "Please provide a YouTube video link."}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=PORT)

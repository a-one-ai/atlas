from flask import Flask, render_template, jsonify, request
from models import proccesVideoFile, proccesYoutubeLinkVideo, proccesAudioFile
import os
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime
from downloaders.downloaders_route import downloader_blueprint

app = Flask(__name__)


# Register the Blueprint with the app
app.register_blueprint(downloader_blueprint)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Adjust cors_allowed_origins as needed



@socketio.on('connect')
def handle_connect():
    print('Client connected')

def genrateUniqueName():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


def send_status_update(message):
    socketio.emit('status_update', {'message': message})


# Configuration
UPLOAD_VIDEOS_FOLDER = r"video"
UPLOAD_AUDIOS_FOLDER = r"audio"
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
    id=genrateUniqueName()   
    try:
        file_path = os.path.join(folder_path, f"{id}"+file.filename)
        print(id)
        file.save(file_path)
        send_status_update("Processing file...")
        result = process_function(file_path)
        #send_status_update("Processed file...")
        os.remove(file_path)
        return jsonify({"data": result})
    except Exception as e:
        print(f"Error {type(e).__name__} occurred: {e}")
        return jsonify({"error": "Internal server error. File processing failed."}), 500

@app.route("/getAudioFile", methods=["POST"])
def process_audio():
    """Process uploaded audio files."""
    audio = request.files.get("audio")
    #print(type(audio))
    print("Audio Downloaded Successfully! ")
    if audio:
        return process_file(audio, UPLOAD_AUDIOS_FOLDER, proccesAudioFile)
    return jsonify({"error": "Invalid audio file. Please upload a valid file."}), 400

@app.route("/getVideoFile", methods=["POST"])
def process_video():
    """Process uploaded video files."""
    video = request.files.get("video")
    # Convert video to audio
    # audio_bytes = convertVideo(video)
    print("Video File Downloaded Successfully! ") 
    if video:
        return process_file(video, UPLOAD_VIDEOS_FOLDER, proccesVideoFile)
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
            tr = json_data["tr"]
        except:
            print("Error in translation json")
        send_status_update("Processing youtube link...")
        result = proccesYoutubeLinkVideo(video_link, tr)
        send_status_update("Processed youtube link...")
        print(result)
        return jsonify({"data": result})
        #except Exception as e:
        #   print(f"Error {type(e).__name__} occurred: {e}")
        #  return jsonify({"error": "Internal server error. YouTube link processing failed."}), 500

    # If no link is provided in either form or JSON
    return jsonify({"error": "Please provide a YouTube video link."}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=PORT, processes=True)

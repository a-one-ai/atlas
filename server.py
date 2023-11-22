from models import proccesVideoAudioFile, proccesYoutubeLinkVideo
from flask import Flask, render_template, jsonify, request, url_for
import os

app = Flask(__name__)
# Define the folder where uploaded videos will be stored
UPLOAD_Videos_FOLDER_PATH = "./uploaded_videos"
# Define the folder where uploaded audios will be stored
UPLOAD_Audios_FOLDER_PATH = "./uploaded_audios"

# Create the upload videos folder if it doesn't exist
if not os.path.exists(UPLOAD_Videos_FOLDER_PATH):
    os.makedirs(UPLOAD_Videos_FOLDER_PATH)

# Create the upload audios folder if it doesn't exist
if not os.path.exists(UPLOAD_Audios_FOLDER_PATH):
    os.makedirs(UPLOAD_Audios_FOLDER_PATH)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/getAudioFile", methods=["POST"])
def audioFileProcessing():
    print(f"request.files : {request.files}")
    if "audio" in request.files:
        audio = request.files["audio"]
        if audio.filename != "":
            try:                
                audio_path = os.path.join(UPLOAD_Audios_FOLDER_PATH, audio.filename)
                audio.save(audio_path)

                result = proccesVideoAudioFile(audio_path)   
                print(f"result : {result}")
                return render_template("audio_display.html", data=result)         
                return jsonify({"data":result})
            except Exception as error:
                print(f"Error {type(error)} occurred while processing the audio: {error}")
                return {"data": "Please, Re-Upload the audio file !!!"}
        else:
            return {"data": "Please, Re-Upload the audio file !"}
    else:
        return {"data": "Only audios are allowed to be uploaded !"}


@app.route("/getVideoFile", methods=["POST"])
def videoFileProcessing():
    if "video" in request.files:
        video = request.files["video"]
        if video.filename != "":
            try:                
                video_path = os.path.join(UPLOAD_Videos_FOLDER_PATH, video.filename)
                video.save(video_path)
                print(f" 1video file path {video_path}")
                result = proccesVideoAudioFile(video_path)  
                return render_template("video_display.html", data=result)          
                return jsonify({"data":result})
            except Exception as error:
                print(f"Error {type(error)} occurred while processing the video: {error}")
                return {"data": "Please, Re-Upload the video file !!!"}
        else:
            return {"data": "Please, Re-Upload the video file !"}
    else:
        return {"data": "Only videos are allowed to be uploaded !"}


@app.route("/getYoutubeVideoLink", methods=["POST"])
def videoLinkProcessing():
    try:
        videoLink = request.form["youtubeVideoLink"]
    except:
        videoLink = request.json.get("link")
    if videoLink:
        try:                
            result = proccesYoutubeLinkVideo(videoLink)  
            return render_template("link_display.html", data=result)          
        except Exception as error:
            print(f"Error {type(error)} occurred while processing the youtube video link: {error}")
            return {"data": "Please, Re-Upload the youtube video link !!!"}

    else:
        return {"data": "Please enter the youtube video link to be processed !"}

port = 8070      
if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug=True,port=port)
    print(f"Server is running at port {port}")

    

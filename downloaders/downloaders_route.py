from flask import Blueprint, jsonify, request, send_file
from downloaders.DriveDownloader import drive_downloader

# Create a Blueprint for all PDF-related routes
downloader_blueprint = Blueprint('downloader', __name__, url_prefix='/downloader')

# Define a route for the function "/pdf" endpoint
@downloader_blueprint.route('/drive', methods=['POST'])
def download_drive():
    
    """Process Drive video links."""
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

        result = drive_downloader(video_link)
        print(result)
        return jsonify({"data": result})
        #except Exception as e:
        #   print(f"Error {type(e).__name__} occurred: {e}")
        #  return jsonify({"error": "Internal server error. YouTube link processing failed."}), 500

    # If no link is provided in either form or JSON
    return jsonify({"error": "Please provide a YouTube video link."}), 400


# Define a route for the function "/pdf" endpoint
@downloader_blueprint.route('/onedrive', methods=['POST'])
def download_onedrive():
    
    """Process OneDrive video links."""
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

        result = drive_downloader(video_link)
        print(result)
        return jsonify({"data": result})
        #except Exception as e:
        #   print(f"Error {type(e).__name__} occurred: {e}")
        #  return jsonify({"error": "Internal server error. YouTube link processing failed."}), 500

    # If no link is provided in either form or JSON
    return jsonify({"error": "Please provide a YouTube video link."}), 400
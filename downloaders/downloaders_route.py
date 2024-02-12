from flask import Blueprint, jsonify, request, send_file
from DriveDownloader import drive_downloader

# Create a Blueprint for all PDF-related routes
downloader_blueprint = Blueprint('downloader', __name__, url_prefix='/downloader')


# Define a route for the function "/pdf" endpoint
@downloader_blueprint.route('/drive', methods=['POST'])
def download_drive():
    # Check if the request has the file part
    return "works", 200
from flask import Blueprint, request, jsonify

from src.Youtube.Comments import YouTubeComments
from src.Youtube.Downloader import YouTubeDownloader

narrative = Blueprint('narrative', __name__)


@narrative.route('/analyze', methods=['POST'])
def analyze_video():
    youtube_url = request.get_json()['youtube_url']

    if not youtube_url:
        return jsonify({"error": "YouTube URL required"}), 400

    try:
        # Step 1: Download audio
        audio_path = YouTubeDownloader.download_audio(youtube_url)

        # Step 2: Get comments
        video_id = youtube_url.split("v=")[1].split("&")[0]
        comments = YouTubeComments().get_video_comments(video_id)

        return jsonify({
            "audio_path": audio_path,
            "comments_sample": comments[:3]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import business_logic

app = Flask(__name__)


@app.route("/create-resource-with-ai/", methods=["POST"])
def create_resource():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data provided"}), 400

    video_id = data["video_id"]

    captions, status = business_logic.get_transcript(video_id)
    if status == 400:
        return captions

    return (
        jsonify({"message": "Lesson created successfully", "captions": captions}),
        200,
    )


def main():
    app.run(host="0.0.0.0", port=8080)

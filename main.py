from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)


@app.route("/transcript/", methods=["POST"])
def get_transcript():
    try:
        video_id = request.args.get("video_id")
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        captions = " ".join([item["text"] for item in transcript])

        return jsonify(captions)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

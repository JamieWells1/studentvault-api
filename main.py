from flask import Flask, request, jsonify
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)
import requests

# Flask app setup
app = Flask(__name__)

# Proxy setup
username = "spcjl3kcj6"
password = "7e8GNrfkD_fdo3eq7Y"
proxy = f"https://{username}:{password}@gate.smartproxy.com:10001"
proxies = {"http": proxy, "https": proxy}


# Custom YouTubeTranscriptApi class to disable SSL verification
class CustomYouTubeTranscriptApi(YouTubeTranscriptApi):
    @classmethod
    def _get_transcripts(cls, video_ids, languages):
        """
        Override the default method to add SSL verification and proxy settings.
        """
        response = requests.get(
            f"https://www.youtube.com/watch?v={video_ids[0]}",
            proxies=proxies,
            verify=False,  # Disable SSL verification
        )
        if response.status_code != 200:
            raise CouldNotRetrieveTranscript("Failed to retrieve the transcript")
        return super()._get_transcripts(video_ids, languages)


# Endpoint to fetch transcript
@app.route("/transcript/", methods=["POST"])
def get_transcript():
    try:
        video_id = request.args.get("video_id")
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        # Use custom API to fetch the transcript
        transcript = CustomYouTubeTranscriptApi.get_transcript(video_id)

        # Combine captions into a single string
        captions = " ".join([item["text"] for item in transcript])

        return jsonify({"captions": captions})

    except TranscriptNotFound:
        return jsonify({"error": "Transcript not found"}), 404
    except CouldNotRetrieveTranscript as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

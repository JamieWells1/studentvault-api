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

# Monkey patch requests.get to disable SSL verification and use the proxy
original_requests_get = requests.get


def custom_requests_get(*args, **kwargs):
    # Set the proxy and disable SSL verification
    kwargs["proxies"] = proxies
    kwargs["verify"] = False
    return original_requests_get(*args, **kwargs)


# Apply the monkey patch
requests.get = custom_requests_get


@app.route("/transcript/", methods=["POST"])
def get_transcript():
    try:
        video_id = request.args.get("video_id")
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        # Fetch the transcript using the patched request
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)

        # Combine captions into a single string
        captions = " ".join([item["text"] for item in transcript])

        return jsonify({"captions": captions})

    except NoTranscriptFound:
        return jsonify({"error": "Transcript not found"}), 404
    except CouldNotRetrieveTranscript as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/proxy-diagnose/", methods=["GET"])
def proxy_diagnose():
    try:
        response = requests.get(
            "https://www.youtube.com/", proxies=proxies, verify=False, timeout=10
        )
        return jsonify(
            {
                "status_code": response.status_code,
                "content_snippet": response.text[:500],
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

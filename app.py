import json

import core.business_logic as business_logic

from flask import Flask, request


app = Flask(__name__)


@app.route("/create-with-ai/", methods=["POST"])
def create_resource():
    data = request.get_json()

    if not data:
        return json.dumps({"error": "no data provided"}), 400

    video_id = data["video_id"]
    print("video id: ", video_id)

    get_captions = json.loads(business_logic.get_transcript(video_id))
    if get_captions["status"] == 400:
        return json.dumps(get_captions["error"])

    return (
        json.dumps(
            {
                "message": "Lesson created successfully",
                "captions": get_captions["captions"],
            }
        ),
        200,
    )


def main():
    app.run(host="0.0.0.0", port=8080)

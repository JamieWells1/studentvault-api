import json

import core.business_logic as business_logic

from flask import Flask, request


app = Flask(__name__)


@app.route("/create-with-ai/", methods=["POST"])
def create_resource():
    data = request.get_json()
    """

    example_request = {
        "video_id": uNeyu46JtIk,
        "generation_method": "video",
        "content": "",
        "resource_type": "lesson",
        }

    """

    error = business_logic.handle_body_errors(data)
    if error:
        return json.dumps({"status": 200, "message": f"Invalid body content: {error}"})

    if data["generation_method"] == "video":
        get_captions = json.loads(business_logic.get_transcript(data["video_id"]))
        if get_captions["status"] == 400:
            return json.dumps({"status": 200, "message": get_captions["error"]})

    return (
        json.dumps(
            {
                "status": 200,
                "message": "Resource created successfully",
                "captions": get_captions["captions"],
            }
        ),
        200,
    )


def main():
    app.run(host="0.0.0.0", port=8080)

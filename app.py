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
        "text_prompt": "",
        "resource_type": "lesson",
        }

    """

    data = business_logic.BodyData(
        video_id=data.get("video_id"),
        generation_method=data.get("generation_method"),
        text_prompt=data.get("text_prompt"),
        resource_type=data.get("resource_type"),
    )

    payload_handler = business_logic.FinalPayload(data)
    final_response = payload_handler.generate()

    return json.dumps(final_response)


def main():
    app.run(host="0.0.0.0", port=8080)

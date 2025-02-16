import json
from typing import Dict, List

from core import business_logic
from core import flashcards
from config.const import PROXY
from utils import logger

from flask import Flask, request


app = Flask(__name__)


# Endpoint for creating AI resources
@app.route("/create-with-ai/", methods=["POST"])
def create_resource():
    data = request.get_json()

    """
    example_request = {
        "video_id": "uNeyu46JtIk",
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

    server = business_logic.Server(data)
    resource = server.generate()

    return json.dumps(resource)


# Endpoint for extracting Quizlet flashcards
@app.route("/extract-flashcards/", methods=["POST"])
def extract_flashcards():
    data = request.get_json()

    extracted_flashcards: List[Dict] = flashcards.extract(data.get("body"))

    return json.dumps(extracted_flashcards)


def main():
    logger.output(f"Running on proxy port {PROXY.get("port")}")
    app.run(host="0.0.0.0", port=8080)

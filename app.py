import json
from typing import Dict, List

from core import server
from core import flashcards
from core.integrations import ai_images
from config.const import PROXY, STUDENTVAULT_API_KEY
from utils import logger
from core.integrations import open_ai
from core.data import Data

from flask import Flask, request


app = Flask(__name__)

data = Data()
data.sync()


# ==================================
#       Resource functionality
# ==================================


# Endpoint for creating AI resources
@app.route("/create-with-ai/", methods=["POST"])
def create_resource():
    request_data = request.get_json()

    """
    example_request = {
        "video_id": "uNeyu46JtIk",
        "generation_method": "video",
        "text_prompt": "",
        "resource_type": "lesson",
        }

    """

    request_data = server.BodyData(
        video_id=request_data.get("video_id"),
        generation_method=request_data.get("generation_method"),
        text_prompt=request_data.get("text_prompt"),
        resource_type=request_data.get("resource_type"),
    )

    service = server.Server(request_data)
    resource = service.generate()

    return json.dumps(resource)


# Endpoint for extracting Quizlet flashcards
@app.route("/extract-flashcards/", methods=["POST"])
def extract_flashcards():
    request_data = request.get_json()

    """
    example_request = {
        "body": "What is another name for stocks/shares? - Equities;
        What is another name for fixed-income? - Bonds;"
        }
    """

    extracted_flashcards: List[Dict] = flashcards.extract(request_data.get("body"))

    return json.dumps(extracted_flashcards)


# Endpoint for generating an image with Replicate
@app.route("/generate-image/", methods=["POST"])
def generate_image():
    request_data = request.get_json()

    """
    example_request = {
        "topic": "Hooke's Law",
        "custom_prompt": "A car suspension system absorbing impact.",
        "prompt_type": "topic",
    }
    """

    response = ai_images.generate_image(
        topic=request_data.get("topic"),
        custom_prompt=request_data.get("custom_prompt"),
        prompt_type=request_data.get("prompt_type"),
    )

    return json.dumps(response)


# ==================================
#       Chat functionality
# ==================================


@app.route("/answer-question/", methods=["POST"])
def answer_question():
    request_data = request.get_json()

    response = open_ai.answer_question(
        question=request_data.get("question"),
        lesson_context=request_data.get("lesson_context"),
    )

    return json.dumps(response)


# ==================================
#       Search/memory functionality
# ==================================


@app.route("/search/", methods=["POST"])
def get_search_results():
    request_data = request.get_json()

    """
    example_request = {
        "resource_type": "ai_quiz",
        "query": "physics resistivity",
    }
    """

    # returns unique ids of all matches found
    return data.search(resource_type, query)


@app.route("/update-cache/", methods=["POST"])
def update_cache():
    request_data = request.get_json()

    """
    example_request = {
        "table": "lesson",
        "unique_id": "1733086015938x643431375464275700",
        "title": "My cool lesson",
        "studentvault_api_key": "1FD3F3A74762DE8DC8272A127",
        }
    """

    if request_data.headers.get("studentvault_api_key") != STUDENTVAULT_API_KEY:
        return {"status": 400, "message": "Unauthenticated request"}

    entry = data.update(table, unique_id, title)
    if entry:
        return {"status": 200, "message": "Entry updated successfully"}
    else:
        # force a resync
        return data.sync()


@app.route("/delete-item/", methods=["POST"])
def delete_item():
    request_data = request.get_json()

    """
    example_request = {
        "table": "lesson",
        "unique_id": "1733086015938x643431375464275700",
        "title": "My cool lesson",
        "studentvault_api_key": "1FD3F3A74762DE8DC8272A127",
        }
    """

    if request_data.headers.get("studentvault_api_key") != STUDENTVAULT_API_KEY:
        return {"status": 400, "message": "Unauthenticated request"}

    entry = data.delete(table, unique_id, title)
    if entry:
        return {"status": 200, "message": "Entry deleted successfully"}
    else:
        # force a resync
        return data.sync()


# ==================================
#       Update cache functionality
# ==================================


# will manually get all the necassary database
# contents from bubble and write to json files
@app.route("/force-sync/", methods=["GET"])
def sync_json_files():
    return data.sync()


# ==================================
#       Run server
# ==================================


def main():
    logger.output(f"Running on proxy port {PROXY.get("port")}")
    app.run(host="0.0.0.0", port=8080)

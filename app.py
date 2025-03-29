import json
from typing import Dict, List

from core import server
from core import flashcards
from core.integrations import ai_images
from config.const import PROXY
from utils import logger
from core.integrations import open_ai

from flask import Flask, request


app = Flask(__name__)

with open("data/modules.json", "r") as module_data:
    modules = json.load(module_data)

with open("data/lessons.json", "r") as lesson_data:
    lessons = json.load(lesson_data)

with open("data/quizzes.json", "r") as quiz_data:
    quizzes = json.load(quiz_data)

with open("data/decks.json", "r") as deck_data:
    decks = json.load(deck_data)


# ==================================
#       Resource functionality
# ==================================


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

    data = server.BodyData(
        video_id=data.get("video_id"),
        generation_method=data.get("generation_method"),
        text_prompt=data.get("text_prompt"),
        resource_type=data.get("resource_type"),
    )

    server = server.Server(data)
    resource = server.generate()

    return json.dumps(resource)


# Endpoint for extracting Quizlet flashcards
@app.route("/extract-flashcards/", methods=["POST"])
def extract_flashcards():
    data = request.get_json()

    """
    example_request = {
        "body": "What is another name for stocks/shares? - Equities;
        What is another name for fixed-income? - Bonds;"
        }
    """

    extracted_flashcards: List[Dict] = flashcards.extract(data.get("body"))

    return json.dumps(extracted_flashcards)


# Endpoint for generating an image with Replicate
@app.route("/generate-image/", methods=["POST"])
def generate_image():
    data = request.get_json()

    """
    example_request = {
        "topic": "Hooke's Law",
        "custom_prompt": "A car suspension system absorbing impact.",
        "prompt_type": "topic",
    }
    """

    response = ai_images.generate_image(
        topic=data.get("topic"),
        custom_prompt=data.get("custom_prompt"),
        prompt_type=data.get("prompt_type"),
    )

    return json.dumps(response)


# ==================================
#       Chat functionality
# ==================================


@app.route("/answer-question/", methods=["POST"])
def answer_question():
    data = request.get_json()

    response = open_ai.answer_question(
        question=data.get("question"),
        lesson_context=data.get("lesson_context"),
    )

    return json.dumps(response)


# ==================================
#       Search functionality
# ==================================


@app.route("/search/", methods=["POST"])
def get_search_results():
    pass


# ==================================
#       Update cache functionality
# ==================================


# will manually get all the necassary database
# contents from bubble and write to json files
@app.route("/force-sync/", methods=["POST"])
def sync_json_files():
    url = "https://studentvault.co.uk/version-test/api/1.1/obj/ai_quiz"
    data = requests.get(url).json()


def main():
    logger.output(f"Running on proxy port {PROXY.get("port")}")
    app.run(host="0.0.0.0", port=8080)

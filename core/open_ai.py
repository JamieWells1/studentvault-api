import json

from config.const import OPENAI_API_KEY, OPENAI_MODEL
import config.response_objects as models
from config.openai_context import Context

from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def create_mc_quiz(text_prompt, generation_method):

    shared_instructions = Context.Quiz.SHARED

    if generation_method == "video":
        instructions = Context.Quiz.VIDEO
    elif generation_method == "text":
        instructions = Context.Quiz.TEXT

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions + shared_instructions,
                },
                {
                    "role": "user",
                    "content": text_prompt,
                },
            ],
            model=OPENAI_MODEL,
            response_format=models.Quiz,
        )
        quiz = json.loads(response.choices[0].message.content)
        quiz["questions"] = remove_extra_answers(quiz["questions"])
        return {"status": 200, "payload": quiz}

    except Exception as e:
        return {"status": 400, "payload": e}


def remove_extra_answers(questions):
    for question in questions:
        answers_to_remove = len(question["wrong_answers"]) - 3
        if answers_to_remove > 0:
            for i in range(1, answers_to_remove + 1):
                question["wrong_answers"].pop(-i)

    return questions


def create_lesson(text_prompt, generation_method):

    shared_instructions = Context.Lesson.SHARED

    if generation_method == "video":
        instructions = Context.Lesson.VIDEO
    elif generation_method == "text":
        instructions = Context.Lesson.TEXT

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions + shared_instructions,
                },
                {
                    "role": "user",
                    "content": text_prompt,
                },
            ],
            model=OPENAI_MODEL,
            response_format=models.Lesson,
        )
        lesson = json.loads(response.choices[0].message.content)
        return {"status": 200, "payload": lesson}

    except Exception as e:
        return {"status": 400, "payload": e}


def create_flashcard_deck(text_prompt, generation_method):

    shared_instructions = Context.FlashcardDeck.SHARED

    if generation_method == "video":
        instructions = Context.FlashcardDeck.VIDEO
    elif generation_method == "text":
        instructions = Context.FlashcardDeck.TEXT

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions + shared_instructions,
                },
                {
                    "role": "user",
                    "content": text_prompt,
                },
            ],
            model=OPENAI_MODEL,
            response_format=models.FlashcardDeck,
        )

        deck = json.loads(response.choices[0].message.content)
        return {"status": 200, "payload": deck}

    except Exception as e:
        return {"status": 400, "payload": e}


# Creates resource from an image. This is currently not being used in production as this uses the vision
# model, which is ~100x more expensive than 4o-mini as of 18/02/2025 ($15, $30 per 1M tokens input, output)
def resource_from_image():

    context = """
        What's in this photo?
        """

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": context},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "",
                            },
                        },
                    ],
                }
            ],
            model="gpt-4o",
        )

        response = response.choices[0].message.content
        return {"status": 200, "payload": response}

    except Exception as e:
        return {"status": 400, "payload": e}

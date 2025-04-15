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


def create_lesson(text_prompt, generation_method, lesson_type):

    instructions = Context.Lesson.LESSON_TYPES[lesson_type]

    if generation_method == "video":
        instructions += Context.Lesson.VIDEO
    elif generation_method == "text":
        instructions += Context.Lesson.TEXT

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions,
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


def answer_question(question, lesson_context):
    instructions = Context.Answer.INSTRUCTIONS

    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": f"""question: {question}, lesson_context: {lesson_context}""",
                },
            ],
            model=OPENAI_MODEL,
            response_format=models.Answer,
        )

        answer = json.loads(response.choices[0].message.content)
        return {"status": 200, "payload": answer}

    except Exception as e:
        return {"status": 400, "payload": e}

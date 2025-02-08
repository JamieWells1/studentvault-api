import json

from config.const import OPENAI_API_KEY, OPENAI_MODEL
import config.response_objects as models

from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def create_mc_quiz(text_prompt, generation_method):

    shared_instructions = """Each question can more than one correct 
    answer, but each question must have exactly 4 answers to choose from 
    in total, including both correct and wrong answers. """

    if generation_method == "video":

        instructions = """You are to create a multiple choice quiz based on the following video transcript. 
        The amount of questions that you create should depend on the length of the video transcript and how 
        much content is covered in the transcript. """

    elif generation_method == "text":

        instructions = """You are to create a multiple choice quiz based on the following text prompt. 
        The amount of questions that you create should depend on how much content the user is looking to cover. """

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
    return quiz

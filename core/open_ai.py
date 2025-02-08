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


def create_lesson(text_prompt, generation_method):

    shared_instructions = """The lesson will contain a mixture of text blocks (which you will use for explaining concepts), 
    multiple choice question blocks and fill in the blanks blocks. Each text block must contain 2-3 sentences, and 
    multiple choice questions must have exactly 4 answers to choose from in total, including 
    both correct and wrong answers. The string returned for each fill in the blank block must have the
    following syntax: 'Protons are made up of two [up quarks/up] and one [down quark/down]', where each blank is 
    represented by a pair of square brackets, and inside the square brackets are the correct answers. 
    There can br more than one correct answer for each blank, and each correct answer should be 
    separated by a forward slash. There can be multiple blanks per string, but never add more than 
    3 blanks to any given string. The lesson should take the user about 5 minutes to complete, and 
    you must follow the following format with the same blocks in the same places: 
    
{
  "blocks": [
    {
      "text": "Introductory explanation"
    },
    {
      "question": "question",
      "wrong_answers": ["Wrong Answer 1", "Wrong Answer 2", "Wrong Answer 3"],
      "correct_answers": ["Correct Answer 1"],
      "explanation": "Explanation"
    },
    {
      "text": "Explanation about Core Concept 1"
    },
    {
      "fill_in_the_blank": "String for fill in the [blank/blanks] with multiple [blank/blanks]"
    },
    {
      "text": "Explanation about Core Concept 2"
    },
    {
      "question": "question",
      "wrong_answers": ["Wrong Answer 1", "Wrong Answer 2", "Wrong Answer 3"],
      "correct_answers": ["Correct Answer 1"],
      "explanation": "Explanation"
    },
    {
      "text": "Explanation about Application Section"
    },
    {
      "question": "question",
      "wrong_answers": ["Wrong Answer 1", "Wrong Answer 2", "Wrong Answer 3"],
      "correct_answers": ["Correct Answer 1"],
      "explanation": "Explanation"
    },
    {
      "text": "Explanation about Recap & Summary"
    },
    {
      "fill_in_the_blank": "String for fill in the [blank/blanks] with multiple [blank/blanks]"
    },
    {
      "fill_in_the_blank": "String for fill in the [blank/blanks] with multiple [blank/blanks]"
    },
    {
      "fill_in_the_blank": "String for fill in the [blank/blanks] with multiple [blank/blanks]"
    }
  ]
}
    """

    if generation_method == "video":
        instructions = (
            """You are to create a lesson based on the transcript provided. """
        )

    elif generation_method == "text":
        instructions = (
            """You are to create a lesson based on the text prompt provided. """
        )

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
    return lesson


def create_flashcard_deck(text_prompt, generation_method):
    pass

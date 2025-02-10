import json

from config.const import OPENAI_API_KEY, OPENAI_MODEL
import config.response_objects as models

from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def create_mc_quiz(text_prompt, generation_method):

    shared_instructions = """Each multiple choice question must have exactly 3 
    wrong answers in the 'wrong_answers' list and each wrong answer must be
    different to the correct answer; there cannot be two of the same option in any given question. 
    It is important that each question is not too easy - answers should be similar in nature in order 
    to make it challenging, but not too similar that it becomes unclear which answer is correct, 
    even if the user knows the answer. """

    if generation_method == "video":
        instructions = """You are to create a multiple choice quiz based on the following video transcript. 
        The amount of questions that you create should depend on the length of the video transcript and how 
        much content is covered in the transcript. You must omit any content you find that is not relevant 
        to the general topic of the video, such as promotions and ads. """

    elif generation_method == "text":
        instructions = """You are to create a multiple choice quiz based on the following text prompt. 
        The amount of questions that you create should depend on how much content the user is looking to cover. """

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

    shared_instructions = """The lesson will contain a mixture of text blocks (which you will use for explaining concepts), 
    multiple choice question blocks and fill in the blanks blocks. For each block, it will have a corresponding section 
    number, which will be in the 'sections' array. For example, if there are 12 items in the 'blocks' array, there must be 12 
    integers in the sections array, each one corresponding to its block counterpart. Each text block must contain 2-3 sentences, and 
    multiple choice questions must have exactly 3 wrong answers in the 'wrong_answers' list, and each wrong answer must be
    different to the correct answer; there cannot be two of the same option in any given question.
    It is important that each question is not too easy - answers should be similar in nature in order 
    to make it challenging, but not too similar that it becomes unclear which answer is correct, 
    even if the user knows the answer. 
    The string returned for each fill in the blank block must have the following syntax: 'Protons are 
    made up of two [up quarks/up] and one [down quark/down]', where each blank is represented 
    by a pair of square brackets, and inside the square brackets are the correct answers. 
    There can be more than one correct answer for each blank, and each correct answer should be 
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
      "correct_answer": "Correct Answer",
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
      "correct_answer": "Correct Answer",
      "explanation": "Explanation"
    },
    {
      "text": "Explanation about Application Section"
    },
    {
      "question": "question",
      "wrong_answers": ["Wrong Answer 1", "Wrong Answer 2", "Wrong Answer 3"],
      "correct_answer": "Correct Answer",
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
  ],
  "sections": [
    1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5
  ]
}
    """

    if generation_method == "video":
        instructions = """You are to create a lesson based on the transcript provided. 
            You must omit any content you find that is not relevant 
            to the general topic of the video, such as promotions and ads. """

    elif generation_method == "text":
        instructions = (
            """You are to create a lesson based on the text prompt provided. """
        )

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

    shared_instructions = """Each flashcard should have a simple front term and back definition. When necassary 
    or when you see fit, make sure to include a short and sweet explanation about why the definition matches 
    up to that specific term. Bear in mind that some users will want flashcards with translations from one 
    language to another, so make sure to include things such as cognates and sentence examples when appropriate. 
    You must make sure that the front of each flashcard is descriptive enough for the user to know what they 
    should be answering. For example, instead of putting 'nuclear fission', put 'what is nuclear fission?'. 
    At the same time, the flashcard is supposed to be quick and each side should not be in full sentences. Rather than 
    'What is the purpose of using different colors in the derivation approach?' on the front and 'Different colors are 
    used in the derivation to visually differentiate steps and enhance understanding.' on the back, it should be 
    'purpose of using different colors in the derivation approach' on the front and 'visually differentiate steps and enhance 
    understanding' on the back. That way, the user can understand what the front of the flashcard is asking whilst 
    not being overwhelmed with text. """

    if generation_method == "video":
        instructions = """You are to create a flashcard deck based on the following video transcript.
        It doesn't matter how many flashcards you generate (unless specified by the user) as the ultimate goal 
        is to cover everything in the transcript. You must omit any content you find that is not relevant 
        to the general topic of the video, such as promotions and ads. """

    elif generation_method == "text":
        instructions = """You are to create a flashcard deck based on the following video transcript.
        It doesn't matter how many flashcards you generate (unless specified by the user) as the ultimate goal 
        is to cover everything in the text prompt. """

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

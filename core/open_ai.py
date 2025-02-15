import json

from config.const import OPENAI_API_KEY, OPENAI_MODEL
import config.response_objects as models

from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def create_mc_quiz(text_prompt, generation_method):

    shared_instructions = """
    You are an expert instructional designer generating quizzes for a learning platform targeted at 
    UK students aged 15-18. For any given quiz, here is the criteria:
    
    Each multiple choice question must have exactly 3 
    wrong answers in the 'wrong_answers' list and each wrong answer must be
    different to the correct answer; there cannot be two of the same option in any given question. 
    It is important that each question is not too easy - answers should be similar in nature in order 
    to make it challenging, but not too similar that it becomes unclear which answer is correct, 
    even if the user knows the answer. The incorrect answers must be plausible but incorrect. 
    Ensure the distractors are relevant to the topic and designed to challenge users without being 
    too easy or absurd. Where possible, distractors must reflect common misconceptions in order to 
    increase difficulty. Based on user feedback, questions with distractor options like 'random guesses' 
    are too easy. Generate a question with well-thought-out distractors that resemble real-world errors 
    or misunderstandings. Here is an example of a good question based on the previously mentioned 
    criteria:
    
    Which of the following explains why plants appear green under normal light conditions?
    a) Green is absorbed by chlorophyll (distractor)
    b) Chlorophyll reflects green light (correct)
    c) Chlorophyll absorbs red and blue light but emits green (distractor)
    d) All light except green is absorbed and stored (distractor)
    """

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

    shared_instructions = """
    You are an expert instructional designer generating lessons for a learning platform targeted at 
    UK students aged 15-18. For any given lesson, here is the criteria:

    The lesson will contain a mixture of text blocks (which you will use for explaining concepts), 
    multiple choice question blocks and fill in the blanks blocks. For each block, it will have a corresponding section 
    number, which will be in the 'sections' array. For example, if there are 12 items in the 'blocks' array, there must be 12 
    integers in the sections array, each one corresponding to its block counterpart. Each text block must contain 2-3 sentences, and 
    multiple choice questions must have exactly 3 wrong answers in the 'wrong_answers' list, and each wrong answer must be
    different to the correct answer; there cannot be two of the same option in any given question.
    It is important that each question is not too easy - answers should be similar in nature in order 
    to make it challenging, but not too similar that it becomes unclear which answer is correct, 
    even if the user knows the answer. The incorrect answers must be plausible but incorrect. 
    Ensure the distractors are relevant to the topic and designed to challenge users without being 
    too easy or absurd. Where possible, distractors must reflect common misconceptions in order to 
    increase difficulty. Based on user feedback, questions with distractor options like 'random guesses' 
    are too easy. Generate a question with well-thought-out distractors that resemble real-world errors 
    or misunderstandings. Here is an example of a good question based on the previously mentioned 
    criteria:
    
    Which of the following explains why plants appear green under normal light conditions?
    a) Green is absorbed by chlorophyll (distractor)
    b) Chlorophyll reflects green light (correct)
    c) Chlorophyll absorbs red and blue light but emits green (distractor)
    d) All light except green is absorbed and stored (distractor)

    The string returned for each fill in the blank block must have the following syntax: 'Protons are 
    made up of two [up] quarks and one [down] quark', where each blank is represented 
    by a pair of square brackets, and inside the square brackets are the correct answers. 
    There can be more than one correct answer for each blank, and each correct answer should be 
    separated by a forward slash. There can be multiple blanks per string, but never add more than 
    3 blanks to any given string. The blanks must always (except when filling in very specific keywords 
    on vary rare occasions) consist of just 1 word (or number) per blank, otherwise it gets way too 
    hard for the user. In blanks where there should be grammar (e.g. apostrophies) and capital letters, 
    add another option to each one which isn't case and grammar sensitive, because the user is unlikely 
    to use correct grammar to fill in the blank, but they shouldn't have to get it wrong just because of that. 
    The lesson should take the user about 5 minutes to complete, and 
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

Here is an example response:

{
  "blocks": [
    {
      "text": "This lesson will cover the concept of Young's modulus, which is a measure of the stiffness of a material. We will explore how to calculate Young's modulus by applying a force to a material and measuring its extension."
    },
    {
      "question": "What is Young's modulus defined as?",
      "wrong_answers": [
        "The ratio of energy to strain",
        "The total stress applied",
        "The force divided by area"
      ],
      "correct_answer": "The ratio of tensile stress to tensile strain",
      "explanation": "Young's modulus is the ratio of tensile stress (force per unit area) to tensile strain (the extension divided by the original length)."
    },
    {
      "text": "To calculate stress, we divide the applied force by the cross-sectional area of the material. Strain is calculated as the extension of the material divided by its original length. The formula for Young's modulus combines these definitions."
    },
    {
      "fill_in_the_blank": "Young's modulus, represented as [E], is equal to the ratio of [stress] to [strain]."
    },
    {
      "text": "When measuring the extension of a wire, precise measurements of the diameter are essential for accurate calculations of the cross-sectional area. The equation for calculating the area from the diameter is Area = π * (Diameter² / 4)."
    },
    {
      "question": "What does the equation for Young's modulus involve?",
      "wrong_answers": [
        "Area multiplied by stress",
        "Force and total length combined",
        "Strain times area"
      ],
      "correct_answer": "Tensile stress and tensile strain",
      "explanation": "The Young's modulus equation involves dividing tensile stress by tensile strain to determine how much a material will deform under a certain stress."
    },
    {
      "text": "In a typical experiment, a mass is added to a wire, causing it to extend. The extension is recorded, and the data can be plotted to find the gradient, which can then be used to calculate Young's modulus for the material."
    },
    {
      "question": "What is the significance of measuring the extension accurately in this experiment?",
      "wrong_answers": [
        "To ensure the wire holds together",
        "To determine the weight of the wire",
        "To calculate the length of the wire"
      ],
      "correct_answer": "To reduce the percentage uncertainty in the measurements",
      "explanation": "Accurate measurements of extension minimize the percentage uncertainty, leading to more reliable calculation of Young's modulus."
    },
    {
      "text": "After obtaining the data for mass and extension, these values can be plotted on a graph. The slope of the line obtained allows for the calculation of Young's modulus through its relationship with tension and strain."
    },
    {
      "fill_in_the_blank": "In this experiment, the extension ([e]) is plotted against the mass ([m]) on the graph to find the gradient, which is used to calculate Young's [modulus]."
    },
    {
      "fill_in_the_blank": "The cross-sectional area (represented by the letter [A]) can be calculated using the formula A = πD²/[4], where [D] is the diameter of the wire."
    },
    {
      "fill_in_the_blank": "To ensure safety, it is important to wear [eye] protection while conducting this experiment, as the wire can store [energy] and may snap."
    }
  ],
  "sections": [
    1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5
  ]
},


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

    shared_instructions = """
    You are an expert instructional designer generating flashcards for a learning platform targeted at 
    UK students aged 15-18. For any given flashcard, here is the criteria:
    
    Each flashcard should have a simple front term and back definition. When necassary 
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

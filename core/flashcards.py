# Used for extracting information about flashcards from Quizlet and importing them into StudentVault

import re
from typing import Dict, List


REGEX_PATTERN = r"([^?-]+) - ([^;]+);"


def extract(body) -> List[Dict]:
    """
    example_request = {
        "body": "What is another name for stocks/shares? - Equities;
        What is another name for fixed-income? - Bonds;"
        }

    """

    raw_flashcards = re.findall(REGEX_PATTERN, body)
    flashcard_fronts = [front.strip() for front, back in raw_flashcards]
    flashcard_backs = [back.strip() for front, back in raw_flashcards]

    flashcards = []

    for i, term in enumerate(flashcard_fronts):
        flashcards.append({"front": flashcard_fronts[i], "back": flashcard_backs[i]})

    return flashcards

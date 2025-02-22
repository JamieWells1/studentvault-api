from typing import Union

from pydantic import BaseModel


# Building blocks


class MultipleChoiceQuestion(BaseModel):
    question: str
    wrong_answers: list[str]
    correct_answer: str
    explanation: str


class FillInTheBlanksQuestion(BaseModel):
    fill_in_the_blank: str


class Text(BaseModel):
    text: str


class Flashcard(BaseModel):
    front: str
    back: str


# Models


class Lesson(BaseModel):
    blocks: list[Union[Text, FillInTheBlanksQuestion, MultipleChoiceQuestion]]
    sections: list[int]
    block_types: list[str]


class FlashcardDeck(BaseModel):
    flashcards: list[Flashcard]


class Quiz(BaseModel):
    questions: list[MultipleChoiceQuestion]


class Module(BaseModel):
    sections: list[Union[Lesson, Quiz, FlashcardDeck]]

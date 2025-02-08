from pydantic import BaseModel


# Building blocks


class MultipleChoiceQuestion(BaseModel):
    question: str
    wrong_answers: list[str]
    correct_answers: list[str]
    explanation: str


class FillInTheBlanksQuestion(BaseModel):
    sentence: str


class Text(BaseModel):
    content: str


class Flashcard(BaseModel):
    front: str
    back: str


# Models


class Lesson(BaseModel):
    blocks: list[Text, FillInTheBlanksQuestion, MultipleChoiceQuestion]


class FlashcardDeck(BaseModel):
    flashcards: list[Flashcard]


class Quiz(BaseModel):
    questions: list[MultipleChoiceQuestion]

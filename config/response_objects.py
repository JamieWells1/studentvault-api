from pydantic import BaseModel

class MultipleChoiceQuestion(BaseModel):
    question: str
    wrong_answers: list[str]
    correct_answers: list[str]

class FillInTheBlanksQuestion(BaseModel):
    sentence: str

class Text(BaseModel):
    content: str

class Lesson(BaseModel):
    blocks: list[Text, FillInTheBlanksQuestion, MultipleChoiceQuestion]

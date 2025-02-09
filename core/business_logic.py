import json
from dataclasses import dataclass

from core.error_handler import ErrorHandler
import core.open_ai as open_ai


@dataclass
class BodyData:
    video_id: str
    generation_method: str
    text_prompt: str
    resource_type: str


class Server:
    def __init__(self, data):
        self.data = data

    def __handle_resource_generation(self, text_prompt):
        # Invoke the right method to create our AI resource
        if self.data.resource_type == "lesson":
            response = open_ai.create_lesson(
                text_prompt=text_prompt, generation_method=self.data.generation_method
            )
            return {
                "status": response["status"],
                "resource_type": self.data.resource_type,
                "payload": response["payload"],
            }

        elif self.data.resource_type == "quiz":
            response = open_ai.create_mc_quiz(
                text_prompt=text_prompt, generation_method=self.data.generation_method
            )
            return {
                "status": response["status"],
                "resource_type": self.data.resource_type,
                "payload": response["payload"],
            }

        elif self.data.resource_type == "flashcard_deck":
            response = open_ai.create_flashcard_deck(
                text_prompt=text_prompt, generation_method=self.data.generation_method
            )
            return {
                "status": response["status"],
                "resource_type": self.data.resource_type,
                "payload": response["payload"],
            }

        return {
            "status": 400,
            "payload": "There were no issues found but OpenAI did not process your request.",
        }

    def generate(self):

        # Error handling
        errors = ErrorHandler(data=self.data)
        handler = errors.handle()

        if handler["status"] == 400:
            errors_found = handler.get("errors")
            error_message = (
                f"Found {len(errors_found)} errors: {', '.join(errors_found)}"
            )
            return {
                "status": handler["status"],
                "payload": error_message,
            }

        # Get prompt text from validation service
        text_prompt = handler["payload"]
        try:
            text_prompt = handler["payload"]["captions"]
        except:
            pass

        return self.__handle_resource_generation(text_prompt)

import json
from dataclasses import dataclass

from core.error_handler import ErrorHandler


@dataclass
class BodyData:
    video_id: str
    generation_method: str
    text_prompt: str
    resource_type: str


class FinalPayload:
    def __init__(self, data):
        self.data = data

    def generate(self):

        # Error handling
        error_handler = ErrorHandler(data=self.data)
        response = error_handler.handle()

        if response["status"] == 400:
            return {
                "status": response["status"],
                "payload": f"Found {len(response["errors"])} errors: {response["errors"]}",
            }

        payload = response["captions"]

        return {
            "status": response["status"],
            "payload": payload,
        }

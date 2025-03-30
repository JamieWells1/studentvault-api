from core.integrations.youtube import Youtube

from typing import List

from config.const import GENERATION_METHODS, RESOURCE_TYPES
from utils import logger


class ErrorHandler:
    def __init__(self, data):
        self.data = data

    def __handle_body_errors(self) -> List[str]:
        errors = []

        if not self.data:
            errors.append("No body data provided")
        elif self.data.generation_method not in GENERATION_METHODS:
            errors.append("Not a valid generation method")
        elif self.data.resource_type not in RESOURCE_TYPES:
            errors.append("Not a valid resource type")
        elif not self.data.video_id and self.data.generation_method == "video":
            errors.append("No video URL provided")
        elif not self.data.text_prompt and self.data.generation_method == "text":
            errors.append("No text prompt provided")

        return errors

    # ============== The function below doubles up as a successful captions fetch. ==============

    # This is so the captions are retrieved only once for each request
    # to avoid YouTube blocking too frequent requests.

    def __handle_get_captions(self) -> List[str]:
        youtube_handler = Youtube(video_id=self.data.video_id)

        logger.output("Awaiting YouTube captions response...")
        captions_response = youtube_handler.get_captions()

        if captions_response["errors"]:
            return {"status": 400, "errors": captions_response["errors"]}

        logger.output("Fetched YouTube captions")
        return {"status": 200, "captions": captions_response["captions"]}

    # Parent handler

    def handle(self) -> List[str]:
        errors = []

        # Handle errors in the request body
        errors.extend(self.__handle_body_errors())

        # Handle errors when fetching captions
        if self.data.generation_method == "video":
            captions_response = self.__handle_get_captions()

            if captions_response.get("errors"):
                errors.extend(captions_response["errors"])
                return {"status": 400, "errors": errors}

            return {"status": 200, "payload": captions_response}

        if errors:
            return {"status": 400, "errors": errors}

        return {"status": 200, "payload": self.data.text_prompt}

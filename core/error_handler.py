from core.youtube import Youtube

from typing import List

GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "multiple_choice_quiz", "flashcards"]


class ErrorHandler:
    def __init__(self, data):
        self.data = data

    def __handle_body_errors(self) -> List[str]:
        errors = []

        if not self.data:
            errors.append("No body data provided")
        elif not self.data.video_id and self.data.generation_method == "video":
            errors.append("No video URL provided when generation type is set to video")
        elif not self.data.text_prompt and self.data.generation_method == "text":
            errors.append("No text prompt when generation type is set to text")
        elif self.data.generation_method not in GENERATION_METHODS:
            errors.append("Not a valid generation method")
        elif self.data.resource_type not in RESOURCE_TYPES:
            errors.append("Not a valid resource type")

        return errors

    # ============== The function below doubles up as a successful captions fetch. ==============

    # This is so the captions are retrieved only once for each request
    # to avoid YouTube blocking too frequent requests.

    def __handle_get_captions(self) -> List[str]:
        youtube_handler = Youtube(video_id=self.data.video_id)

        captions_response = youtube_handler.get_captions()

        if captions_response["errors"]:
            return {"status": 400, "errors": captions_response["errors"]}

        return {"status": 200, "captions": captions_response["captions"]}

    def __handle_openai_errors(self) -> List[str]:
        errors = []

        return errors

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

        # Handle errors when forming OpenAI response
        errors.extend(self.__handle_openai_errors())

        if errors:
            return {"status": 400, "errors": errors}
        return captions_response

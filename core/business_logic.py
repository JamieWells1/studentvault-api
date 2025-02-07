import json

from config.const import PROXY

from youtube_transcript_api import YouTubeTranscriptApi

GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "multiple_choice_quiz", "flashcards"]


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, proxies={"https": PROXY["url"], "http": PROXY["url"]}
        )
        captions = " ".join([item["text"] for item in transcript])

        response = {"status": 200, "captions": captions}
        return json.dumps(response)

    except Exception as e:
        response = {"error": f"Couldn't get video transcript: {e}", "status": 400}
        return json.dumps(response)


def handle_body_errors(data):
    if not data:
        return "No body data provided"
    elif not data.get("video_id") and data.get("generation_method") == "video":
        return "No video URL provided when generation type is set to video"
    elif not data.get("text_prompt") and data.get("generation_method") == "text":
        return "No text prompt when generation type is set to text"
    elif data.get("generation_method") not in GENERATION_METHODS:
        return "Not a valid generation method"
    elif data.get("resource_type") not in RESOURCE_TYPES:
        return "Not a valid resource type"

    return None

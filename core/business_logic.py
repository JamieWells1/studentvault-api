import json

from config.env_vars import PROXY

from youtube_transcript_api import YouTubeTranscriptApi


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

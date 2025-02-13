from config.const import PROXY

from youtube_transcript_api import YouTubeTranscriptApi


class Youtube:
    def __init__(self, video_id):
        self.video_id = video_id
        self.error_messages = {
            "invalid_url": "The video URL you provided either isn't a valid URL or the video doesn't support captions.",
        }

    def get_captions(self):
        errors = []
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                self.video_id, proxies={"https": PROXY["url"], "http": PROXY["url"]}
            )
            captions = " ".join([item["text"] for item in transcript])

            return {"status": 200, "captions": captions, "errors": []}

        except Exception as e:
            errors.append(str(e))

        return {"status": 400, "errors": errors}

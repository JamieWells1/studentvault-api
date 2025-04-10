import random

from youtube_transcript_api import YouTubeTranscriptApi
from utils import logger


class Youtube:
    def __init__(self, video_id):
        self.video_id = video_id
        self.error_messages = {
            "invalid_url": "The video URL you provided either isn't a valid URL or the video doesn't support captions.",
        }

        # Proxy config
        __username = "user-spcjl3kcj6-sessionduration-5"
        __password = "P+s3l3g2xBXe5dlnRo"
        self.sticky_port = self.__get_random_port()

        self.PROXY = {
            "url": f"http://{__username}:{__password}@gate.smartproxy.com:{self.sticky_port}",
            "port": self.sticky_port,
        }

    def get_captions(self):
        errors = []
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                self.video_id,
                proxies={"https": self.PROXY["url"], "http": self.PROXY["url"]},
            )
            captions = " ".join([item["text"] for item in transcript])

            if len(captions) > 30000:
                raise Exception("Video too long. Try again with a different video.")

        except Exception as e:
            errors.append(str(e))
            logger.error(str(e))

        else:
            logger.output(f"Captions retrieved from video with ID '{self.video_id}'")
            return {"status": 200, "captions": captions, "errors": []}

        return {"status": 400, "errors": errors}

    def __get_random_port(self) -> str:
        port = str(random.randint(1, 999))
        port = "10" + ("0" * (3 - len(port))) + port
        logger.output(f"Proxy running on port {port}")

        return port

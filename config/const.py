import os
import random


port = str("100" + str(random.randint(10, 99)))
print(port)

__username = "spcjl3kcj6"
__password = "P+s3l3g2xBXe5dlnRo"

PROXY = {
    "url": f"http://{__username}:{__password}@gate.smartproxy.com:{port}",
}

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "quiz", "flashcard_deck"]

import os
import random


# Start the server with a random proxy port or the rotating port
sticky_port = str("100" + str(random.randint(10, 99)))
ROTATING_PORT = 7000


# Environment variables
__username = "user-spcjl3kcj6-sessionduration-5"
__password = "P+s3l3g2xBXe5dlnRo"


# Proxy URL
PROXY = {
    "url": f"http://{__username}:{__password}@gate.smartproxy.com:{sticky_port}",
    "port": sticky_port,
}


# Endpoints
DEV_RESOURCE_URL = "http://127.0.0.1:8080/create-with-ai/"
PROD_RESOURCE_URL = "https://youtube-captions-api.onrender.com/create-with-ai/"

DEV_EXTRACT_FLASHCARDS_URL = "http://127.0.0.1:8080/extract-flashcards/"
PROD_EXTRACT_FLASHCARDS_URL = (
    "https://youtube-captions-api.onrender.com/extract-flashcards/"
)


# OpenAI environment variables and model
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"


# Enums available to server
GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "quiz", "flashcard_deck"]

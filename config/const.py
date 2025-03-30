import os
import random


# Endpoints
DEV_RESOURCE_URL = "http://127.0.0.1:8080/create-with-ai/"
PROD_RESOURCE_URL = "https://youtube-captions-api.onrender.com/create-with-ai/"

DEV_EXTRACT_FLASHCARDS_URL = "http://127.0.0.1:8080/extract-flashcards/"
PROD_EXTRACT_FLASHCARDS_URL = (
    "https://youtube-captions-api.onrender.com/extract-flashcards/"
)


# API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")

# Authentication key for handling cache
STUDENTVAULT_API_KEY = "1FD3F3A74762DE8DC8272A127"

# Models
OPENAI_MODEL = "gpt-4o-mini"
REPLICATE_MODEL = "black-forest-labs/flux-schnell"

# Enums available to server
GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "quiz", "flashcard_deck"]

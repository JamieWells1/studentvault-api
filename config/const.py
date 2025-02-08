import os
import random


# Start the server with a random proxy port
port = str("100" + str(random.randint(10, 99)))
print(f"Using port {port}")

# Environment variables
__username = "spcjl3kcj6"
__password = "P+s3l3g2xBXe5dlnRo"

# Proxy URL
PROXY = {
    "url": f"http://{__username}:{__password}@gate.smartproxy.com:{port}",
}

# Endpoints
DEV_URL = "http://127.0.0.1:8080/create-with-ai/"
PROD_URL = "https://youtube-captions-api.onrender.com/create-with-ai/"

# OpenAI environment variables and model
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# Enums available to server
GENERATION_METHODS = ["text", "video"]
RESOURCE_TYPES = ["lesson", "quiz", "flashcard_deck"]

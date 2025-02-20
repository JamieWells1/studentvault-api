import requests
import json
import random

from tests import test_endpoint
from config.const import DEV_RESOURCE_URL, PROD_RESOURCE_URL


video_ids = [
    "uNeyu46JtIk",
    "HXW2tRfTkTE",
    "nFWJZRx6GDA",
    "gdWqkw9A-pI",
    "L1WMvTiAt4E",
    "nKxpEHBDMjQ",
]

# If video_id should be none this is a placeholder
selected_id = video_ids[random.randint(0, len(video_ids) - 1)]

video_id = selected_id
generation_method = "text"
text_prompt = "Robert J. Oppenheimer"
resource_type = "quiz"

headers = {"Content-Type": "application/json"}
body = {
    "video_id": video_id,
    "generation_method": generation_method,
    "text_prompt": text_prompt,
    "resource_type": resource_type,
}

response = test_endpoint.send_request(DEV_RESOURCE_URL, headers, body)

print(
    f"\n========================== Response: ==========================\n\n{response.text}\n"
)

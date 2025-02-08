import requests
import json
import random

import tests.test_endpoint as endpoint
from config.const import DEV_URL, PROD_URL


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
text_prompt = "18th century privateering"
resource_type = "quiz"

headers = {"Content-Type": "application/json"}
body = {
    "video_id": video_id,
    "generation_method": generation_method,
    "text_prompt": text_prompt,
    "resource_type": resource_type,
}

response = endpoint.send_request(DEV_URL, headers, body)

print(
    f"\n========================== Response: ==========================\n\n{response.text}\n"
)

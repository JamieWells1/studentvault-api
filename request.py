import requests
import json
import random

import tests.test_endpoint as endpoint

DEV_URL = "http://127.0.0.1:8080/create-with-ai/"
PROD_URL = "https://youtube-captions-api.onrender.com/create-with-ai/"


video_ids = [
    "uNeyu46JtIk",
    "HXW2tRfTkTE",
    "nFWJZRx6GDA",
    "gdWqkw9A-pI",
    "L1WMvTiAt4E",
    "nKxpEHBDMjQ",
]

video_id = video_ids[random.randint(0, len(video_ids) - 1)]
headers = {"Content-Type": "application/json"}
body = {
    "video_id": video_id,
    "generation_method": "video",
    "text_prompt": "Generate me a cool lesson on electricity",
    "resource_type": "lesson",
}

response = endpoint.send_request(DEV_URL, headers, body)

print("Status Code:", response.status_code)
print("Response:", response.text)

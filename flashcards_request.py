import requests
import json

from tests import test_endpoint
from config.const import DEV_EXTRACT_FLASHCARDS_URL

headers = {"Content-Type": "application/json"}
body = {
    "body": "What is another name for stocks/shares? - Equities; What is another name for fixed-income? - Bonds;"
}

response = test_endpoint.send_request(DEV_EXTRACT_FLASHCARDS_URL, headers, body)

print(
    f"\n========================== Response: ==========================\n\n{response.text}\n"
)

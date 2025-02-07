import requests
import json

url = "http://127.0.0.1:8080/create-with-ai/"
headers = {"Content-Type": "application/json"}
body = {"video_id": "OB99E7Y1cMA"}

response = requests.post(url, headers=headers, json=body)

print("Status Code:", response.status_code)
print("Response:", response.text)

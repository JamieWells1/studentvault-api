import requests


def send_request(url, headers, body):
    response = requests.post(url, headers=headers, json=body)
    return response

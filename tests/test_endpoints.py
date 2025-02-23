import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import requests
import json

from utils import logger

BASE_URL = "http://0.0.0.0:8080"


def test_create_resource():
    """Test the /create-with-ai/ endpoint"""
    url = f"{BASE_URL}/create-with-ai/"

    # Test data
    payload = {
        "video_id": "uNeyu46JtIk",
        "generation_method": "video",
        "text_prompt": "",
        "resource_type": "lesson",
    }

    response = requests.post(url, json=payload)
    logger.output("Create Resource Test")
    logger.output(f"Status Code: {response.status_code}")
    logger.output(f"Response: {json.dumps(response.json(), indent=2)}")

    return response


def test_extract_flashcards():
    """Test the /extract-flashcards/ endpoint"""
    url = f"{BASE_URL}/extract-flashcards/"

    # Test data
    payload = {
        "body": """
        What is another name for stocks/shares? - Equities; 
        What is another name for fixed-income? - Bonds;
        """
    }

    response = requests.post(url, json=payload)
    logger.output("Extract Flashcards Test")
    logger.output(f"Status Code: {response.status_code}")
    logger.output(f"Response: {json.dumps(response.json(), indent=2)}")

    return response


def test_generate_image():
    """Test the /generate-image/ endpoint"""
    url = f"{BASE_URL}/generate-image/"

    # Test with topic
    topic_payload = {
        "topic": "Hooke's Law",
        "custom_prompt": "",
        "prompt_type": "topic",
    }

    # Test with custom prompt
    custom_prompt_payload = {
        "topic": "",
        "custom_prompt": "A car suspension system absorbing impact.",
        "prompt_type": "custom_prompt",
    }

    logger.output("Generate Image Test (Topic)")
    response = requests.post(url, json=topic_payload)
    logger.output(f"Status Code: {response.status_code}")
    logger.output(f"Response: {json.dumps(response.json(), indent=2)}")

    logger.output("Generate Image Test (Custom Prompt)")
    response = requests.post(url, json=custom_prompt_payload)
    logger.output(f"Status Code: {response.status_code}")
    logger.output(f"Response: {json.dumps(response.json(), indent=2)}")

    return response


if __name__ == "__main__":
    logger.output("Running endpoint tests...")

    tests_passed = 0

    try:
        response = test_create_resource()
        if response.status_code == 200:
            tests_passed += 1

        response = test_extract_flashcards()
        if response.status_code == 200:
            tests_passed += 1

        response = test_generate_image()
        if response.status_code == 200:
            tests_passed += 1

    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the server.")
        logger.output("Make sure your Flask server is running on http://localhost:8080")
    except Exception as e:
        logger.error(f"{e}")

    logger.output(f"Tests passed: {tests_passed}/3")

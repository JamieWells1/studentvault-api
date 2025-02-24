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


def test_answer_question():
    """Test the /answer-question/ endpoint"""
    url = f"{BASE_URL}/answer-question/"

    # Test data
    payload = {
        "question": "I really don't understand how plants can just make energy from sunlight",
        "lesson_context": "{'blocks': [{'text': 'Photosynthesis is the process by which green plants use sunlight to convert carbon dioxide and water into glucose and oxygen. This essential biological process supports life on Earth by providing food for plants and oxygen for animals.'}, {'question': 'What are the two main stages of photosynthesis?', 'wrong_answers': ['Light reactions and photorespiration', 'Calvin cycle and respiration', 'Light-dependent reactions and fermentation'], 'correct_answer': 'Light-dependent reactions and the Calvin cycle', 'explanation': 'Photosynthesis consists of two main stages: the light-dependent reactions that capture sunlight and the Calvin cycle which synthesizes glucose.'}, {'text': 'Core Concept 1: The light-dependent reactions take place in the thylakoid membranes of chloroplasts and convert solar energy into chemical energy in the form of ATP and NADPH.'}, {'fill_in_the_blank': 'In the light-dependent reactions, [solar] energy is transformed into [chemical] energy.'}, {'text': 'Core Concept 2: The Calvin cycle, also known as the light-independent reactions, uses ATP and NADPH from the light-dependent reactions to convert carbon dioxide into glucose.'}, {'question': 'What does the Calvin cycle primarily produce?', 'wrong_answers': ['Oxygen', 'ATP', 'Heat'], 'correct_answer': 'Glucose', 'explanation': 'The Calvin cycle uses the products of the light-dependent reactions to fix carbon dioxide and produce glucose.'}, {'text': 'Application: Understanding photosynthesis is key to improving agricultural productivity and developing sustainable energy solutions. Researchers focus on optimizing this process to increase crop yields and biofuel production.'}, {'question': 'Why is studying photosynthesis important for agriculture?', 'wrong_answers': ['To improve pest resistance', 'To alter soil composition', 'To increase biodiversity'], 'correct_answer': 'To enhance crop yield', 'explanation': 'Advancements in the understanding of photosynthesis can lead to better farming practices that maximize growth efficiency and yield.'}, {'text': 'Recap: Photosynthesis is vital for life on Earth, converting light energy into chemical energy. The process has two main stages: light-dependent reactions and the Calvin cycle, crucial for plant growth and oxygen production.'}, {'fill_in_the_blank': 'Photosynthesis is expressed as [6CO2 + 6H2O -> C6H12O6 + 6O2] showing the conversion of [carbon dioxide] and [water] into glucose and oxygen.'}, {'fill_in_the_blank': 'The green pigment involved in photosynthesis is [chlorophyll] which absorbs light energy.'}, {'fill_in_the_blank': 'Plants mainly perform photosynthesis in [chloroplasts], specialized organelles within their cells.'}], 'sections': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5], 'block_types': ['text', 'question', 'text', 'fill_in_the_blank', 'text', 'question', 'text', 'question', 'text', 'fill_in_the_blank', 'fill_in_the_blank', 'fill_in_the_blank']}",
    }

    response = requests.post(url, json=payload)
    logger.output("Answer Question Test")
    logger.output(f"Status Code: {response.status_code}")
    logger.output(f"Response: {json.dumps(response.json(), indent=2)}")


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

        response = test_answer_question()
        if response.status_code == 200:
            tests_passed += 1

    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the server.")
        logger.output("Make sure your Flask server is running on http://localhost:8080")
    except Exception as e:
        logger.error(f"{e}")

    logger.output(f"Tests passed: {tests_passed}/3")

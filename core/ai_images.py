import os
from typing import Dict

from config.const import REPLICATE_MODEL, REPLICATE_API_KEY
from utils import logger

import replicate

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


# Either topic or custom_prompt must be provided
def generate_image(
    topic: str = "", custom_prompt: str = "", prompt_type: str = "topic"
) -> Dict[str, str]:
    client = replicate.Client(api_token=REPLICATE_API_KEY)

    try:
        output = client.run(
            REPLICATE_MODEL,
            input={
                "seed": 0,
                "prompt": get_prompt(topic, custom_prompt, prompt_type),
                "go_fast": True,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "webp",
                "output_quality": 80,
                "num_inference_steps": 4,
            },
        )

        # If the environment is production, output[0] is the image URL
        # If the environment is development, output[0] is the image object
        if ENVIRONMENT == "production":
            image_url = output[0]
        else:
            image_url = output[0].url
        logger.output(f"Image URL: {image_url}")

    except Exception as e:
        logger.error(f"{e}")
    else:
        return {"status": 200, "image_url": image_url}

    return {"status": 400, "error": f"Failed to generate image: {e}"}


def get_prompt(
    topic: str, custom_prompt: str = None, prompt_type: str = "topic"
) -> str:
    if custom_prompt and prompt_type == "custom_prompt":
        return f"""
        A highly detailed, photorealistic image of {custom_prompt}. 
        The image should capture a practical, real-life scenario where this concept is naturally observed. 
        The scene should be immersive, with realistic lighting, textures, and depth of field. Avoid any artificial 
        elements, text, labels, or diagrams—focus purely on an authentic, real-world depiction of {custom_prompt}.

        The image must be grounded in reality and must not be abstract, symbolic, or artistic interpretations—it 
        should depict something a person could see in real life.

        Important: Do not reference or take inspiration from any of the following examples—these are strictly to 
        illustrate the level of detail and realism required:

        🚗 For physics concepts, like Hooke's Law → A car suspension system absorbing impact.
        🌱 For biology, like Photosynthesis → A microscopic view of chloroplasts inside a leaf.
        🌍 For geography, like Tectonic Plate Movement → A cracked fault line after an earthquake.
        🏭 For history, like The Industrial Revolution → Workers in a steam-powered factory.

        These examples should not influence your image—only ensure that the generated image follows the same level 
        of photorealism, clarity, and realism.
        """
    elif topic and prompt_type == "topic":
        return f"""
        A highly detailed, photorealistic image of a real-world application of {topic}. 
        The image should capture a practical, real-life scenario where this concept is naturally observed. 
        The scene should be immersive, with realistic lighting, textures, and depth of field. Avoid any artificial 
        elements, text, labels, or diagrams—focus purely on an authentic, real-world depiction of {topic} in action.

        The image must be grounded in reality and must not be abstract, symbolic, or artistic interpretations—it 
        should depict something a person could see in real life.

        Important: Do not reference or take inspiration from any of the following examples—these are strictly to 
        illustrate the level of detail and realism required:

        🚗 For physics concepts, like Hooke's Law → A car suspension system absorbing impact.
        🌱 For biology, like Photosynthesis → A microscopic view of chloroplasts inside a leaf.
        🌍 For geography, like Tectonic Plate Movement → A cracked fault line after an earthquake.
        🏭 For history, like The Industrial Revolution → Workers in a steam-powered factory.

        These examples should not influence your image—only ensure that the generated image follows the same level 
        of photorealism, clarity, and realism.
        """
    else:
        raise ValueError("Either a topic or custom prompt must be provided")

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
            Generate a highly detailed, photorealistic image of {custom_prompt}.
            The image must accurately depict only what is described in {custom_prompt} and nothing else. Do not incorporate elements from unrelated concepts, contexts, or prior examples.

            The scene should be immersive, with realistic lighting, textures, and depth of field. Avoid any artificial elements, text, labels, or diagrams—focus purely on an authentic, real-world depiction.

            Strict Adherence to Context:

            If {custom_prompt} describes a specific time period, environment, or style (e.g., "a medieval blacksmith's workshop"), the image must reflect that and nothing else.
            If {custom_prompt} specifies an artistic style (e.g., "a cartoon of Medusa for young children"), then the entire image must be a cohesive cartoon illustration with no photorealistic elements.
            If {custom_prompt} describes a specific perspective, such as "a close-up of an insect pollinating a flower," then ensure the focus remains solely on that scene with no unrelated background elements.
            Clarifications to Avoid Misinterpretations:
            🚫 Do not use past examples as reference for content—use them only as a guide for quality, realism, and visual coherence.
            🚫 Do not mix themes, time periods, or styles that are not explicitly stated in {custom_prompt}.
            🚫 Do not include abstract, symbolic, or artistic elements unless explicitly requested.

            Final Check: Before finalizing the image, ensure that every detail aligns perfectly with {custom_prompt} and no external context has influenced the output.
        """

    elif topic and prompt_type == "topic":
        return f"""
            Generate a highly detailed, photorealistic image of {topic}.
            The image must accurately depict only what is described in {topic} and nothing else. Do not incorporate elements from unrelated concepts, contexts, or prior examples.

            The scene should be immersive, with realistic lighting, textures, and depth of field. Avoid any artificial elements, text, labels, or diagrams—focus purely on an authentic, real-world depiction.

            Strict Adherence to Context:

            If {topic} describes a specific time period, environment, or style (e.g., "a medieval blacksmith's workshop"), the image must reflect that and nothing else.
            If {topic} specifies an artistic style (e.g., "a cartoon of Medusa for young children"), then the entire image must be a cohesive cartoon illustration with no photorealistic elements.
            If {topic} describes a specific perspective, such as "a close-up of an insect pollinating a flower," then ensure the focus remains solely on that scene with no unrelated background elements.
            Clarifications to Avoid Misinterpretations:
            🚫 Do not use past examples as reference for content—use them only as a guide for quality, realism, and visual coherence.
            🚫 Do not mix themes, time periods, or styles that are not explicitly stated in {topic}.
            🚫 Do not include abstract, symbolic, or artistic elements unless explicitly requested.

            Final Check: Before finalizing the image, ensure that every detail aligns perfectly with {topic} and no external context has influenced the output.
        """
    else:
        raise ValueError("Either a topic or custom prompt must be provided")

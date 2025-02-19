# Playground file for streaming - not being used in resource generation as unable
# to pass baseModel into chat.completions.create(), which is required for streaming

from config.const import OPENAI_API_KEY, OPENAI_MODEL
from config.openai_context import Context
import config.response_objects as models

from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def generate():
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Write me a poem about Smaug the Stupendous",
                }
            ],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

    except Exception as e:
        return {"status": 400, "payload": e}

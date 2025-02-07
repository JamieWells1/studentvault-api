from openai import OpenAI
from config.const import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def send_request():
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say 'StudentVault is the best!'",
            }
        ],
        model="gpt-4o-mini",
    )

    return completion

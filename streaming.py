from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)


def generate():
    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": instructions + shared_instructions,
                },
                {
                    "role": "user",
                    "content": text_prompt,
                },
            ],
            model=OPENAI_MODEL,
            response_format=models.Quiz,
        )
        quiz = json.loads(response.choices[0].message.content)
        quiz["questions"] = remove_extra_answers(quiz["questions"])
        return {"status": 200, "payload": quiz}

    except Exception as e:
        return {"status": 400, "payload": e}

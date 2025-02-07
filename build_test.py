import core.open_ai as open_ai


def test_openai_request():
    completion = open_ai.send_request()
    print(completion.choices[0].message.content)


test_openai_request()

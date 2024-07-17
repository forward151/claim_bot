from openai import OpenAI

GPT_TOKEN = ""

client = OpenAI(
    api_key=GPT_TOKEN,
    base_url="https://api.vsegpt.ru/v1",
)


def get_response(req):
	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "user",
			 "content": req}
		]
	)

	return response.choices[0].message.content

print(get_response("Сколько будет 5+5"))
from openai import OpenAI
client = OpenAI()

response = client.responses.create( # type: ignore
    model="gpt-5",
    reasoning={"effort": "low"},
    input=[
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },
        {
            "role": "user",
            "content": "Tell me about the gamma constant"
        }
    ]
)

print(response.output_text)
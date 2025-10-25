from openai import OpenAI
client = OpenAI()

response = client.responses.create( # type: ignore
    model="gpt-5",
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
    input="Tell me about the gamma constant",
)

print(response.output_text)
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5", #"gpt-4o-mini",
    tools=[{"type":"web_search"}], # type: ignore
    input="What’s a recent event reported in the Australian news today?"
)
print(response.output_text)
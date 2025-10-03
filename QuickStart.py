from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Write a short bedtime story of no more than about 100 words about excessive showering in cold water")


#print(response.output_text)

# Print out the entire response as JSON
print(response.model_dump_json(indent=2))

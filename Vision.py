from openai import OpenAI
import base64, os

client = OpenAI()

image_path = r"C:\Users\grobl\OneDrive\Python\OpenAI\Kookaburra.jpg"
with open(image_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

data_url = f"data:image/jpeg;base64,{img_b64}"

response = client.responses.create(
    model="gpt-5",  # or a vision-capable 4.x model
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "What is the nearest big object in the image? how far?"},
            {"type": "input_image", "image_url": data_url}
        ],
    }], # type: ignore
)

print(response.output_text)

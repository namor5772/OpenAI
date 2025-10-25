from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

resp = client.responses.parse(
    model="gpt-5",
    instructions="Extract the event information.",
    input="Roman and Lee-Ann are going to Mogo Zoo for Lion Viewing next Monday.",
    text_format=CalendarEvent,
)

event: CalendarEvent = resp.output_parsed # type: ignore

# >>> actually print something <<<
print(event)                # pretty __repr__
print(event.model_dump())   # dict
print(event.model_dump_json(indent=2))  # JSON

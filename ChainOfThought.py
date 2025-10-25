from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve the system of three linear equations in three unknowns: 8x + 7y +z = -23, 5x - 4y + 5z = 2, 3x + 6y - 2z = 14"},
    ],
    text_format=MathReasoning,
)

math_reasoning = response.output_parsed

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console()

# Safely unpack the parsed output
math_reasoning = response.output_parsed

console.rule("[bold blue]Step-by-Step Solution[/bold blue]")

for i, step in enumerate(math_reasoning.steps, start=1): # type: ignore
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(f"Step {i}", justify="left", style="cyan")
    table.add_column("Details", justify="left", style="white")
    table.add_row("Explanation", step.explanation)
    table.add_row("Output", step.output)
    console.print(table)

console.rule("[bold green]Final Answer[/bold green]")
console.print(f"[bold yellow]{math_reasoning.final_answer}[/bold yellow]") # type: ignore

# QuickStart.py

This repository contains a minimal example of calling the OpenAI Responses API with the Python SDK. The script, , creates an  client and requests a short bedtime story from the  model, then prints the full JSON response.

## Prerequisites

- Python 3.9 or newer
- An OpenAI API key with access to the  model
- The  Python package ()

Set your API key in the environment before running the script:



On Windows PowerShell:



## Running the example

1. Install dependencies:

   

2. Execute the script:

   

   The script prints the entire API response as formatted JSON. Uncomment the  print statement if you only want the model's textual reply.

## Customizing the request

- Change the  field to target a different model that your account can access.
- Edit the  prompt to generate other types of content.
- Inspect other fields available on the  object to explore metadata returned by the API.

## Troubleshooting

- **Authentication errors**: Double-check that  is set in your environment.
- **Model not found**: Ensure your API key has access to the specified model or switch to one you can use.
- **Network issues**: Retry the request; transient errors are sometimes resolved with a second attempt.

Refer to the [OpenAI Python SDK documentation](https://github.com/openai/openai-python) for more details on available options and best practices.

import os

from openai import OpenAI

import whatsapp_manager

OPENAI_API_KEY = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(message):
    messages = [{"role": "user", "content": message}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_image",
                "description": "Generates an image for a given prompt",
            }
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            available_functions = {
                "generate_image": _generate_image(message)
            }
            function_name = tool_call.function.name

            func_response = available_functions[function_name]
            return func_response, "image"

    return response_message.content, "text"


def _generate_image(prompt):
    response = client.images.generate(prompt=prompt, response_format="url", model="dall-e-3")
    return response.data[0].url

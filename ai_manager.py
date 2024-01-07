import json
import os
from openai import OpenAI
from dotenv import load_dotenv

from models.response_type import RESPONSE_TYPE

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(prompt):
    prompt_response = generate_completion(prompt, use_tools=True)
    tool_calls = prompt_response.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name

            func_response = None
            response_type = None

            if function_name == "generate_image":
                func_response = _generate_image(prompt)
                response_type = RESPONSE_TYPE.IMAGE.value
            elif function_name == "generate_audio":
                func_response = _generate_audio(prompt)
                response_type = RESPONSE_TYPE.AUDIO.value

            return func_response, response_type

    return prompt_response.content, RESPONSE_TYPE.TEXT.value


def get_messages(prompt, system):
    messages = None
    if system:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": prompt}]
    return messages


def _generate_image(prompt):
    response = client.images.generate(prompt=prompt, response_format="url", model="dall-e-3")
    return response.data[0].url


def _generate_audio(prompt):
    response_content = generate_completion(prompt, system="Don't dwell on the fact that you"
                                                          " can't sing or speak. Just give the content "
                                                          "of the prompt without saying you can't do it.").content
    response = client.audio.speech.create(response_format="mp3", input=response_content, model="tts-1", voice="nova")
    response.stream_to_file("output.mp3")
    return response_content


def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "generate_image",
                "description": "Generates an image for a given prompt",
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_audio",
                "description": "Generate an audio/song response to the user's prompt, "
                               "taking into account whether the user wants an audio response.",
            }
        }
    ]


def generate_completion(prompt, system=None, use_tools=False):
    response = None
    gpt_model = "gpt-4"
    prompts = get_messages(prompt, system)
    print(prompts)
    if use_tools:
        response = client.chat.completions.create(
            model=gpt_model,
            messages=prompts,
            tools=get_tools(),
            tool_choice="auto",
        )
    else:
        response = client.chat.completions.create(
            model=gpt_model,
            messages=prompts
        )

    return response.choices[0].message

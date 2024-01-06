import json
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from openai import OpenAI

import ai_manager
import whatsapp_manager

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=OPENAI_API_KEY)

application = Flask(__name__)

WEBHOOK_ENDPOINT = '/whatsapp/webhook'


@application.route(WEBHOOK_ENDPOINT, methods=['POST'])
def receive_new_message():
    data = request.json
    if whatsapp_manager.is_new_message(data):
        phone, message = whatsapp_manager.get_message_from_data(data)
        response_message, response_type = ai_manager.generate_response(message)
        whatsapp_manager.send_response_message(response_message=response_message,
                                               phone=phone, response_type=response_type)

    return "OK"


@application.route(WEBHOOK_ENDPOINT)
def accept_webhook_handshake():
    return request.args.get('hub.challenge', '')


if __name__ == '__main__':
    application.run(debug=True)

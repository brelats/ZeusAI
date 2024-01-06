import threading

from flask import Flask, request, send_from_directory
from dotenv import load_dotenv


import ai_manager
import whatsapp_manager
from models.response_type import RESPONSE_TYPE

load_dotenv()

application = Flask(__name__)
WHATSAPP_BASE_ENDPOINT = 'whatsapp'
WEBHOOK_ENDPOINT = '/whatsapp/webhook'
AUDIO_ENDPOINT = '/whatsapp/audio'


def handle_message(data):
    if whatsapp_manager.is_new_message(data):
        phone, message = whatsapp_manager.get_message_from_data(data)
        whatsapp_manager.send_response_message(response_message="Procesando respuesta...",
                                               phone=phone, response_type=RESPONSE_TYPE.TEXT.value)
        response_message, response_type = ai_manager.generate_response(message)
        whatsapp_manager.send_response_message(response_message=response_message,
                                               phone=phone, response_type=response_type)


@application.route(WEBHOOK_ENDPOINT, methods=['POST'])
def receive_new_message():
    data = request.json
    threading.Thread(target=handle_message, args=(data,)).start()
    return "OK"


@application.route(WEBHOOK_ENDPOINT)
def accept_webhook_handshake():
    return request.args.get('hub.challenge', '')


@application.route(AUDIO_ENDPOINT)
def get_mp3():
    return send_from_directory('', 'output.mp3')


if __name__ == '__main__':
    application.run(debug=True)

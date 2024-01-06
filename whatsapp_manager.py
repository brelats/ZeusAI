import os

import requests
import json

from models.response_type import RESPONSE_TYPE

GRAPH_VERSION = os.getenv('GRAPH_VERSION')
PHONE_ID = os.getenv('PHONE_ID')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
BACKEND_ENDPOINT = os.getenv('BACKEND_ENDPOINT')


def is_new_message(data):
    message_data = _extract_message_data(data)
    print(message_data)
    return message_data is not None


def get_message_from_data(data):
    message_data = _extract_message_data(data)
    if message_data:
        phone = message_data.get('from')
        message = message_data.get('body')
        return phone, message


def _extract_message_data(data):
    try:
        entries = data.get('entry', [])
        for entry in entries:
            changes = entry.get('changes', [])
            for change in changes:
                message = change.get('value', {}).get('messages', [])[0]
                if message:
                    return {
                        'from': message.get('from'),
                        'body': message.get('text', {}).get('body')
                    }
    except (IndexError, TypeError):
        pass
    return None


def send_response_message(response_message, phone, response_type=RESPONSE_TYPE.TEXT.value):
    _post_message_to_whatsapp(response_message, phone, response_type)


def _post_message_to_whatsapp(response_message, phone, response_type):
    url = f'https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_ID}/messages'
    data = {
        'messaging_product': 'whatsapp',
        'to': str(phone),
        'type': response_type,
    }

    if response_type == RESPONSE_TYPE.TEXT.value:
        data[RESPONSE_TYPE.TEXT.value] = {'body': response_message}
    elif response_type == RESPONSE_TYPE.IMAGE.value:
        data[RESPONSE_TYPE.IMAGE.value] = {'link': response_message}
    elif response_type == RESPONSE_TYPE.AUDIO.value:
        data[RESPONSE_TYPE.AUDIO.value] = {'link': f'{BACKEND_ENDPOINT}whatsapp/audio'}

    print(data)
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.reason)
    except requests.RequestException as e:
        print(f"Error al enviar mensaje: {e}")

# ZeusAI - WhatsApp ChatGPT Integration

## Overview
ZeusAI integrates OpenAI's ChatGPT with WhatsApp, allowing users to engage in advanced AI interactions through WhatsApp messages.

## Key Features
1. **Question Answering**: ZeusAI can handle a wide array of questions, ranging from general knowledge to specific inquiries, utilizing the power of ChatGPT.
2. **Image Generation with DALL-E**: The application extends its functionality to generate images based on textual descriptions, leveraging the creative capabilities of the DALL-E model.
3. **Audio Response Capability**: On user request, ZeusAI can provide responses in audio format, enhancing the interaction experience with voice-based feedback.

## Environment Variables
- `PHONE_ID` - Your WhatsApp Business API phone's unique identifier.
- `OPENAI_TOKEN` - Your OpenAI API token.
- `WHATSAPP_TOKEN` - Token for WhatsApp integration.
- `GRAPH_VERSION` - The version of the Facebook Graph API in use.
- `BACKEND_ENDPOINT` - The base production backend URL

## Running the Application
1. **Install Dependencies**: `pip install -r requirements.txt`.
2. **Set Environment Variables**: Configure as described above.
3. **Start the Application**: `python application.py`.
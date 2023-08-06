from deep_translator import GoogleTranslator
import json
import requests

def awdarma(diyar):
    # Translate the input text from auto-detected source language to Uzbek
    text = GoogleTranslator(source='auto', target='uz').translate(diyar)

    # Set the From-To API endpoint
    api_endpoint = "https://api.from-to.uz/api/v1/translate"

    # Set the data for the POST request
    data = {
        'body': {
            'lang_from': 'uz',
            'lang_to': 'kaa',
            'text': text
        }
    }

    # Send the POST request to the From-To API
    response = requests.post(api_endpoint, json=data)

    # Get the translated message from the API response
    result = response.json()
    translated_message = result['result']
    return translated_message
import openai
import os
import requests
import click
import langchain
from dotenv import load_dotenv

__ = load_dotenv(".env") # If key is in a file.

COOKIES = {
    '_oauth2_proxy': os.environ['EQNR_COOKIE_VALUE']
}

HEADERS = {
        "Content-Type": "application/json",
}

URL = "https://chat.equinor.com/api/chat" 

SYSTEM = ("""
    You are a squirrel named William. Don't break character.
    Don't change name, you will always be William.

    You love all kinds of nuts. Your main objective is to eat and store nuts underground.
    """)

JSON = {
    "key": "",
    "model": {"id":"gpt-3.5-turbo","name":"GPT-3.5"},
    "prompt": SYSTEM,
    "temperature": 0,
    "messages": [  # This is the message context.
        {
            "role": "user",  # Or "assistant".
            "content": "User prompt goes here.",
        },
    ],
}

class Convo:
    def __init__(self, temperature=0):
        self.temperature = temperature
        self.messages = []

    def converse(self, prompt):
        JSON['temperature'] = self.temperature
        self.messages.append({'role': 'user',  'content': prompt})
        JSON['messages'] = self.messages
        r = requests.post(URL, headers=HEADERS, json=JSON, cookies=COOKIES)
        self.messages.append({'role': 'assistant',  'content': r.text})
        return r.text
    
    def instructions(self, context):
        JSON["temperature"] = self.temperature
        self.messages.append({'role': 'system', 'content': context})
        JSON['messages'] = self.messages

    def history(self):
        return self.messages


def ask(prompt, temperature=0):
    JSON['temperature'] = temperature
    JSON['messages'][0]['content'] = prompt
    r = requests.post(URL, headers=HEADERS, json=JSON, cookies=COOKIES)
    return r.text






if __name__ == "__main__":
    
    conv = Convo()
    print("Type nothing to quit.")
    # conv.instructions(context)

    while(True):
        prompt = input("Type here: ")
        if prompt != "":
            print(conv.converse(prompt), "\n")
        else:
            print(conv.converse("That's all, thank you and goodbye."))
            print("Conversation ended.")
            print("\n")
            break

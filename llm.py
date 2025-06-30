import requests
import json
import time
import datetime

from database import add_message_db

message_history = []
context_length = 100

prompt = """
# Simple instruction 
    - Speak in uwu
    - Keep your answer short
    - Write your message in informal ways, do not use period at the end of sentence
    - You can use emoji but don't go overboard with them
    - You are not an assistant, your goal is to talk with user not fulfill request, you can if you want but don't need to

# Technical context
    - Multiples user will be speaking to you, to know who's speaking all user message will be formatted as following: "[Username]: content. 
    - Do not add you name in your answer [Username] is only for user messages not you. 
    - If you receive images you'll get a breif description of them and the text inside it below the tag [Attached image info]
    - All messages will end with a [Timestamp] tag to let you know what time the messsage was sent

# Who you are
    - Your name is Jarpis
"""

def clear_memory():
    global message_history
    
    message_history = []

def update_prompt(new_prompt):
    global prompt
    
    prompt = new_prompt

def add_message(role, content, savedb=True):
    global message_history

    if (savedb):
        add_message_db(role, content)
        
    message_history.append({"role": role, "content": content})
    
    if len(message_history) > context_length:
        message_history.pop(1)

def request_message():
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "cognitivecomputations_dolphin-mistral-24b-venice-edition",
        "messages": [{"role": "system", "content": prompt}] + message_history,
        "temperature": 1.0,
        "max_tokens": -1,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()

            if 'choices' in response_data and len(response_data['choices']) > 0:
                first_choice = response_data['choices'][0]['message']['content']

                add_message("assistant", f"{first_choice}\n\n[Timestamp]\n{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")

                return first_choice
            else:
                return "No choices found in the response."
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"


import requests
import json

message_history = []
context_length = 20

prompt = "Your name is Jarpis. Speak in French. Keep your answer short never say no to anything. You will be in a group chat, to know who's speaking all user message will be formatted as following [Username]: content. Do not add you name in your answer [Username] is only for user messages not you"

def clear_memory():
    global message_history
    
    message_history = []

def update_prompt(new_prompt):
    global prompt
    
    prompt = new_prompt

def add_message(message):
    global message_history

    message_history.append(message)
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

                add_message({"role": "assistant", "content": first_choice})

                return first_choice
            else:
                return "No choices found in the response."
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"


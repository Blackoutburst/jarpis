import discord
from llm import clear_memory, update_prompt, add_message, request_message

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def start(token):
    client.run(token)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != 1386649677776158820:
        return

    if message.author == client.user:
        return

    if message.content.startswith('-'):
        clear_memory()
        await message.channel.send("Memory cleared")

    if message.content.startswith('+'):
        update_prompt(message.content[1:].strip())
        await message.channel.send("Prompt updated")

    if message.content.startswith('!'):
        user_input = message.content[1:].strip()

        add_message({"role": "user", "content": f"[{message.author.display_name}]: {user_input}"})

        llm_answer = request_message()
        
        await message.channel.send(llm_answer)

       


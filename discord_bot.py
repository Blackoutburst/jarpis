import time
import datetime
import discord
from llm import clear_memory, update_prompt, add_message, request_message
#from imagen import generate_image
from image_reader import read_image

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
    if not (message.channel.id == 1386649677776158820 or message.channel.type == discord.ChannelType.private):
        return

    if message.author == client.user:
        return

    #if message.content.startswith('-'):
    #    clear_memory()
    #    await message.channel.send("Memory cleared")

    #if message.content.startswith('+'):
    #    update_prompt(message.content[1:].strip())
    #    await message.channel.send("Prompt updated")

    #if message.content.startswith('.'):
    #    filename = generate_image(message.content[1:].strip())
    #    with open(filename, 'rb') as f:
    #        picture = discord.File(f)
    #    await message.channel.send(file=picture)
        
    if message.content.startswith('!') or message.channel.type == discord.ChannelType.private:
        user_input = message.content[1:].strip() if message.content.startswith('!') else message.content

        image_descriptions = []

        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_path = f"/tmp/{attachment.filename}"
                await attachment.save(image_path)

                image_info = read_image(image_path)
                image_descriptions.append(image_info)

        image_summary = "\n".join(image_descriptions)
        full_message = f"[{message.author.display_name}]: {user_input}"
        
        if image_summary:
            full_message += f"\n\n[Attached image info]\n{image_summary}"

        add_message("user", f"{full_message}\n\n[Timestamp]\n{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")

        llm_answer = request_message()
        
        for i in range(0, len(llm_answer), 2000):
            await message.channel.send(llm_answer[i:i+2000])

       


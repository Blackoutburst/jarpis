import argparse
from discord_bot import start
from database import create_db, get_messages_db
from llm import add_message

def main(args):
    create_db()
    msgs = get_messages_db()

    for m in msgs:
        add_message(m[0], m[1], False)
        
    discord_token = args.token
    start(discord_token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str, help="The discord bot token")
    args = parser.parse_args()
    main(args)


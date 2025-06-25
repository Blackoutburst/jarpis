import argparse

from discord_bot import start


def main(args):
    start(args.token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str, help="The discord bot token")
    args = parser.parse_args()
    main(args)


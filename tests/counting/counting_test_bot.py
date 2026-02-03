from email import message
import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

import time

load_dotenv()
token = os.getenv("COUNTING_TEST_BOT_TOKEN")

import signal
import sys

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content: str = message.content
    
    if content.isnumeric():
        time.sleep(2)
        await message.channel.send(int(content) + 1)

def shutdown_handler(sig, frame):
    print("Bot wird beendet...")
    
    print(f"Database connection can be closed here: {__file__}")
    # Database().db.close()

    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_handler)  # kill

bot.run(token)

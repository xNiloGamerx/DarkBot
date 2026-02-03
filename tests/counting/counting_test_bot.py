import discord
from discord.ext import commands

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

    if message.content.startswith('hello'):
        await message.channel.send(f'Hello {message.author.name}!')

    await bot.process_commands(message)

def shutdown_handler(sig, frame):
    print("Bot wird beendet...")
    
    print(f"Database connection can be closed here: {__file__}")
    # Database().db.close()

    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_handler)  # kill

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

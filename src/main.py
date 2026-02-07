import discord
from discord.ext import commands

import logging
from dotenv import load_dotenv
import os

import signal
import sys

from api.connection import SupabaseConnection

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='./log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

extensions = [
    "cogs.core.startup",
    "cogs.members.events",
    "cogs.counting.commands.counting_commands",
    "cogs.counting.events.new_number",
    "cogs.commands.privacy.privacy_commands"
]

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send(f'Hello {message.author.name}!')

    await bot.process_commands(message)

@bot.event
async def setup_hook():
    bot.supabase_connection = await SupabaseConnection()._create_connection()

    for ext in extensions:
        await bot.load_extension(ext)

def shutdown_handler(sig, frame):
    print("Bot wird beendet...")
    
    print(f"Database connection can be closed here: {__file__}")
    # Database().db.close()

    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, shutdown_handler)  # kill

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

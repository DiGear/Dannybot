import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

lastusedcommand = "none"  # defining this for the message handler code
lastsentimage = "none"
intents = discord.Intents.default()

client = commands.Bot(command_prefix=commands.when_mentioned_or(
    'd.', 'D.'), status=discord.Status.dnd, activity=discord.Activity(name="for d.help", type=3), intents=intents, help_command=None)

client.lavalink_nodes = [
{"host": "lava.link", "port": 80, "password": "dismusic"},
]


@client.event
async def on_ready():
    print("Dannybot Music booted successfully")
    print("-------------------------------------")  # prints separator


@client.event
async def on_message(input):
    await client.process_commands(input)

client.load_extension('dismusic')
client.run(os.getenv("TOKEN"))  # start the bot

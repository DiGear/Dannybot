import discord
import os
import sys
import random
import subprocess
import asyncio
import datetime

from discord import File, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from subprocess import call
from threading import Thread
from time import sleep

intents = discord.Intents().all()

#bot setup. sets the command prefix, status, and the game that the bot plays
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    status=discord.Status.online,
    activity=discord.Activity(name="the crewmates", type=3),
    intents=intents,
    help_command=None,
)


#this handles all of the messages the bot sees.
@client.event
async def on_message(message):
  await client.process_commands(message)

#this event triggers ONLY if the bot goes online
@client.event
async def on_ready():
  #displays success message in the terminal, with other useful bot information
 print(client.user.name + " booted successfully")
 print("with ID " + str(client.user.id))
 print('Running on Discord.py Version: {}'.format(discord.__version__))
 print("------------------")

@client.command()
async def m(ctx):
       vc = client.get_channel(1028847589170360453)
       for member in vc.members:
        await member.edit(mute=True)

@client.command()
async def um(ctx):
       vc = client.get_channel(1028847589170360453)
       for member in vc.members:
        await member.edit(mute=False)

@client.command()
async def umg(ctx):
       vc = client.get_channel(1028848221457494066)
       for member in vc.members:
        await member.edit(mute=False)


#this turns on the bot
client.run ('NzU2NjAxMTA3MTI3NzMwMjA2.G0-WFy.3SjoMSKJC4a2XVtKJTMfB5JPFzEr_wLg1-poNI')

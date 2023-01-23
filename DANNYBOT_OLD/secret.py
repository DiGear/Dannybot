import asyncio
import datetime
import hashlib
import json
import os
import random
import re
import sys
import textwrap
import time
import typing
import urllib
import urllib.request
from asyncio import sleep
from collections import namedtuple
from datetime import datetime
from urllib.parse import urlencode

import aiohttp
import audioread
import desktopmagic
import discord
import ffmpeg
import furl
import GPUtil
import imageio
import picopt
import PIL
import praw
import psutil
import pyautogui
import regex
import requests
import wmi
from discord import FFmpegPCMAudio, File, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from discord.utils import get
from gpuinfo import GPUInfo
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)
from PyDictionary import PyDictionary
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from random_word import RandomWords, Wordnik
from wand.display import display as mag_display
from wand.image import Image as magick

from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')

dictionary = PyDictionary()


class Secret(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: secret")

    @commands.command(hidden=True)
    async def eez(self, ctx):  # funny enough this doesnt even check for "d.eez nuts" just "d.eez"
        await ctx.reply("goteem", mention_author=True)

    @commands.command(hidden=True)
    async def bruh(self, ctx):
        await ctx.reply("https://www.youtube.com/watch?v=beQMZ9-Ovs4", mention_author=True)

    @commands.command(hidden=True)
    async def taur_add(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        blacklist = [206392667351941121, 343224184110841856]
        if not ctx.author.id in blacklist:
            await ctx.send("You are not whitelisted for this command!")
            return
        else:
            if(File_Url == "File_Is_Attachment"):
                Link_To_File = ctx.message.attachments[0].url
            else:
                Link_To_File = File_Url
            await ctx.send("Downloading...")

            # this code block writes the image data to a file
            with open("I:\\Dannybot\\cogs\\InternalFiles\\Taurs\\Dooter.png", 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            os.rename("I:\\Dannybot\\cogs\\InternalFiles\\Taurs\\Dooter.png", "I:\\Dannybot\\cogs\\InternalFiles\\Taurs\\" +
                      hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest() + ".png")
            await ctx.send("File Downloaded!")

    @commands.command(hidden=True)
    async def taur(self, ctx):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\Taurs"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'Taur.png'), mention_author=True)
            print("sent Taur: " + file_name)

    @commands.command(hidden=True)
    async def poopoo(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            print("sent file: " + file_name)
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            print("sent file: " + file_name)


async def setup(client):
    await client.add_cog(Secret(client))

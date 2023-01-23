import asyncio
import base64
import datetime
import io
import json
import logging
import os
import pathlib
import random
import re
import subprocess
import sys
import textwrap
import time
import traceback
import typing
import urllib
import urllib.request
from asyncio import sleep
from datetime import datetime

import aiohttp
import discord
import ffmpeg
import imageio
import numpy
import PIL
import psutil
import requests
from discord import FFmpegPCMAudio, File, Member, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import *
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from discord.utils import get
from dotenv import load_dotenv
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)

load_dotenv()

inprocess = True
global processing
processing = False

global request_is_processing
request_is_processing = False

lastusedcommand = "none"
lastsentimage = "none"
intents = discord.Intents.all()

API = "https://backend.craiyon.com/generate"
FORMAT = "png"
TIMEOUT = 10800


async def generate_images(prompt: str) -> str(io.BytesIO):
    async with aiohttp.ClientSession() as session:
        async with session.post(API, json={"prompt": prompt}) as response:
            if response.status == 200:
                print("Dalle server is OK")
                response_data = await response.json()
                images = [
                    io.BytesIO(base64.decodebytes(bytes(image, "utf-8")))
                    for image in response_data["images"]
                ]
                return images
            else:
                return None


def make_collage_sync(images: str(io.BytesIO), wrap: int) -> io.BytesIO:
    image_arrays = [numpy.array(PIL.Image.open(image)) for image in images]
    image_ct = 1
    for image in images:
        print(str(image_ct) + " image(s) generated out of " + str(image_ct))
        image_ct += 1
        image.seek(0)
    collage_horizontal_arrays = [
        numpy.hstack(image_arrays[i: i + wrap])
        for i in range(0, len(image_arrays), wrap)
    ]
    collage_array = numpy.vstack(collage_horizontal_arrays)
    collage_image = Image.fromarray(collage_array)
    collage = io.BytesIO()
    collage_image.save(collage, format=FORMAT)
    print("Attempting to generate 3x3")
    collage.seek(0)
    return collage


async def make_collage(images: str(io.BytesIO), wrap: int) -> io.BytesIO:
    images = await asyncio.get_running_loop().run_in_executor(
        None, make_collage_sync, images, wrap
    )
    print("3x3 Generated")
    return images

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("d.", "D."),
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=3),
    intents=intents,
    help_command=None,
)


@client.event
async def on_ready():
    print("Dannybot Dalle booted successfully")
    print("-------------------------------------")


@client.event
async def on_message(input):
    await client.process_commands(input)


@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, "on_error"):
        return
    ignored = (commands.CommandNotFound,)
    if isinstance(error, ignored):
        return


@client.command()
async def dalle(ctx, *, prompt):
    images = None
    attempt = 0
    print(f'Dalle command ran with prompt "{prompt}"')
    while not images:
        if attempt > 0:
            print(
                f'Image generate request failed on attempt {attempt} for prompt "{prompt}"'
            )
        attempt += 1
        images = await generate_images(prompt)
        print(
            f'Successfully started image generation with prompt "{prompt}" on attempt {attempt}'
        )
        prompt_hyphenated = prompt.replace(" ", "-")
        collage = await make_collage(images, 3)
        b = collage
        collage = discord.File(
            collage, filename=f"{prompt_hyphenated}.{FORMAT}")
        print("Sending image...")
        await ctx.reply(file=collage, mention_author=True)
        print("Caching image...")
        with open("I:\\Dannybot\\cogs\\cache\\dalle.png", "wb") as f:
            b.seek(0)
            f.write(b.read())
            f.close
            print("Image Cache successful")
            print("-------------------------------------")


client.run(os.getenv("TOKEN"))
import asyncio
import datetime
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
from datetime import datetime

import aiohttp
import audioread
import desktopmagic
import discord
import ffmpeg
import GPUtil
import imageio
import openai
import picopt
import PIL
import psutil
import pyautogui
import regex
import requests
import wandb
from discord import FFmpegPCMAudio, File, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from discord.utils import get
from gpuinfo import GPUInfo
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from wand.display import display as mag_display
from wand.image import Image as magick

from fifteen import FifteenAPI
from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')


global request_is_processing
request_is_processing = False
tts_api = FifteenAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")


class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: ai")

    @commands.command(
        aliases=['15', '15tts'],
        description="Sends AI sentences using a very real and legitimate 15.ai API.",
        brief="Use 15.ai to generate funny sentences"
    )
    async def fifteen(self, ctx, *, msg):

        def check(msg):
            return msg.author == ctx.author

        global request_is_processing
        blacklist = [1, 2]
        if ctx.author.id in blacklist:
            await ctx.send("You've been blacklisted from this command")
            return

        else:

            if request_is_processing is True:
                await ctx.reply(
                    "Please allow the previous synthesis to finish.",
                    delete_after=10,
                    mention_author=True,
                )
                return

            try:
                await ctx.send('Which voice would you like? (It is case sensitive!)')
                # 30 seconds to reply
                msgfunc = await self.client.wait_for("message", check=check, timeout=30)
                requested_speaker = msgfunc.content
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")
                return

            await ctx.send("Processing... This could take a while...")
            request_is_processing = True

        tts_api.save_to_file(f"{requested_speaker}", f"{msg}", "output.wav")
        await ctx.reply(file=discord.File(r"output.wav"), mention_author=True)

        await ctx.send("This command is powered by 15.ai ^^^ https://twitter.com/fifteenai")
        request_is_processing = False
        return

    @commands.command(
        aliases=['upscale'],
        description="Locally run waifu2x using speed-optimized settings and send the results.",
        brief="Upscale images using waifu2x"
    )
    async def waifu(self, ctx, *args):
        # this checks to see if the image is an attachment or a link
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Upscaling. Please wait...")

        # this code block writes the image data to a file
        with open(f'I:\\Dannybot\\cogs\\dependencies\\Waifu2x\\w2xinput.png', 'wb') as f:
            f.write(requests.get(Link_To_File).content)
            f.close
        # cd into waifu2x
        os.system('cd I:\\Dannybot\\cogs\\dependencies\\Waifu2x')
        # set the entire python dir to the waifu2x folder
        os.chdir("I:\\Dannybot\\cogs\\dependencies\\Waifu2x")
        # runs the waifu2x AI in cmd
        os.system(
            "waifu2x-caffe-cui.exe -i w2xinput.png -o w2xoutput.png -m noise_scale --scale_ratio 2 --noise_level 2 -x")
        os.chdir("I:\\Dannybot\\cogs\\dependencies\\Waifu2x")
        with open(f'w2xoutput.png', 'rb') as f:  # prepare the file for sending
            try:
                await ctx.reply(file=File(f, 'waifu2x.png'))  # send the file
            except:
                # send this when the image is over 8mb
                await ctx.reply("The image requested is too large to send through discord. Please ask the bot owner to send it to you", mention_author=True)
        f.close  # close the file
        os.chdir('I:\\Dannybot')

    @commands.command(
        aliases=['quote'],
        description="Sends AI generated quotes using the inspirobot API.",
        brief="Get AI generated inspirational posters"
    )
    async def inspire(self, ctx):
        link = "http://inspirobot.me/api?generate=true"
        f = requests.get(link)
        File_Url = f.text
        img = PIL.Image.open(requests.get(File_Url, stream=True).raw)
        img.save("I:\\Dannybot\\cogs\\cache\\quote.jpg", "JPEG")
        f2 = discord.File(
            "I:\\Dannybot\\cogs\\cache\\quote.jpg", filename="quote.jpg")
        embed = discord.Embed(color=0xffc7ed)
        embed.set_image(url="attachment://quote.jpg")
        embed.set_footer(text="Powered by https://inspirobot.me/")
        await ctx.reply(file=f2, embed=embed, mention_author=True)

    @commands.command(
        aliases=['GPT3'],
        description="Interact with GPT3 using Dannybot.",
        brief="Get AI generated text based on provided prompts"
    )
    async def write(self, ctx, *, prompt):
        gpt_prompt = str("write me " + str(prompt))
        print(gpt_prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        await ctx.reply("```" + response['choices'][0]['text'] + "```", mention_author=True)

    @commands.command(
        aliases=['4chan'],
        description="Interact with GPT3 using Dannybot to generate greentexts.",
        brief="Get AI generated greentexts based on provided prompts"
    )
    async def greentext(self, ctx, *, prompt):
        gpt_prompt = str("write me a funny 4chan greentext\n>be me\n" + str(prompt))
        print(gpt_prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        await ctx.reply('```diff\n' + str(prompt).replace('>','+ >') + str(response['choices'][0]['text']).replace('>','+ >') + '```', mention_author=True)


async def setup(client):
    await client.add_cog(AI(client))

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

wordnik_service = Wordnik()
dictionary = PyDictionary()

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: misc")

    @commands.command(
        description="Use a custom flamingtext.com api to generate logos using random presets.",
        brief="Generate a logo with a random font."
    )
    async def logo(self, ctx, *, logotext: typing.Optional[str] = "Your Text Here"):
        logolist = [
            "clan",
            "neon",
            "fluffy",
            "water",
            "smurfs",
            "style",
            "runner",
            "blackbird",
            "fabulous",
            "glow",
            "chrominium",
            "amped",
            "supermarket",
            "crafts",
            "fire",
            "steel",
            "glossy",
            "fifties",
            "retro",
            "beauty",
            "birdy",
            "inferno",
            "winner",
            "uprise",
            "global",
            "silver",
            "minions",
            "magic",
            "fancy",
            "orlando",
            "fortune",
            "swordfire",
            "roman",
            "golden",
            "outline",
            "funtime",
        ]
        # choose a random type from the array
        logotype = random.choice(logolist)

    # add the text to the end of a flamingtext image url
        url = (
            "https://flamingtext.com/net-fu/proxy_form.cgi?script="
            + str(logotype)
            + "-logo&text="
            + str(logotext)
            + "&_loc=generate&imageoutput=true"
        )
        url = furl.furl(url).url
        await ctx.reply(url, mention_author=True)  # send link to image
        print("sent logo")

    @commands.command(
        description="Generate a custom Undertale-Styled textbox by defining the character and text to be said.",
        brief="Generate a custom Undertale-Styled textbox"
        )
    async def undertext(self, ctx, CharacterName, *, Text):
        if(Text.endswith("_ _")):
            Text = "%20"
        url = ("https://www.demirramon.com/gen/undertale_text_box.png?text=" +
               str(Text) + "&character=" + str(undertext(CharacterName)))
        url = furl.furl(url).url
        image = urllib.request.URLopener()
        print(url)
        image.retrieve(url, 'I:\\Dannybot\\cogs\\cache\\undertextout.png')

        await ctx.reply(file=File('I:\\Dannybot\\cogs\\cache\\undertextout.png'), mention_author=True)
        print("sent undertext")

    @commands.command(hidden=True)
    @commands.has_role("fruit")
    async def fruit(self, ctx):
        fruits = ["Apple", "Banana", "Cherry", "Grape", "Mango", "Orange", "Strawberry", "Watermelon", "Kiwi", "Lemon", "Pineapple", "Blueberry", "Raspberry", "Peach", "Lychee", "Cantaloupe", "Plum", "Papaya", "Starfruit", "Honeydew", "Grapefruit", "Durian", "Avocado", "Jackfruit", "Tangerine", "Coconut", "Fig", "Date", "Kumquat", "Persimmon", "Pomegranate"]
        for member in ctx.guild.members:
            try:
                await member.edit(nick=random.choice(fruits))
            except:
                print('rename failed')
    
    @commands.command(hidden=True)
    @commands.has_role("unfruit")
    async def unfruit(self, ctx):
        fruits = ["Apple", "Banana", "Cherry", "Grape", "Mango", "Orange", "Strawberry", "Watermelon", "Kiwi", "Lemon", "Pineapple", "Blueberry", "Raspberry", "Peach", "Lychee", "Cantaloupe", "Plum", "Papaya", "Starfruit", "Honeydew", "Grapefruit", "Durian", "Avocado", "Jackfruit", "Tangerine", "Coconut", "Fig", "Date", "Kumquat", "Persimmon", "Pomegranate"]
        for member in ctx.guild.members:
            try:
                if any(fruit in member.nick for fruit in fruits):
                    await member.edit(nick=None)
            except:
                print('rename failed')


    @commands.command(
        name="8ball", 
        description="Ask Dannybot a question and he will respond with one of many answers.",
        brief="Ask a question and get an answer"
    )
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(
        description="Generate a custom Deltarune-Styled textbox by defining the character and text to be said.",
        brief="Generate a custom Deltarune-Styled textbox"
        )
    async def deltatext(self, ctx, CharacterName, *, Text):
        if(Text.endswith("_ _")):
            Text = "%20"
        url = ("https://www.demirramon.com/gen/undertale_text_box.png?text=" + str(Text) +
               "&mode=darkworld&box=deltarune&character=" + str(undertext(CharacterName)))
        url = furl.furl(url).url
        image = urllib.request.URLopener()
        print(url)
        image.retrieve(url, 'I:\\Dannybot\\cogs\\cache\\undertextout.png')

        await ctx.reply(file=File('I:\\Dannybot\\cogs\\cache\\undertextout.png'), mention_author=True)
        print("sent undertext")

    @commands.command(
        description="Display dictionary entries for a specified word.",
        brief="Display dictionary entries for a specified word"
        )
    async def define(self, ctx, word):
        definition = dictionary.meaning(str(word))
        embed = discord.Embed(color=0xf77e9a)
        embed.add_field(name="Meaning(s):", value=str(definition)
                        .replace("'Noun'", "**Noun**\n")
                        .replace("'Verb'", "**Verb**\n")
                        .replace("'Adverb'", "**Adverb**\n")
                        .replace("'Adjective'", "**Adjective**\n")
                        .replace("'],", "]\n\n")
                        .replace(": ['", "['")
                        .replace("{", "")
                        .replace("}", ""), inline=True)
        await ctx.reply(embed=embed, mention_author=True)

    @commands.command(
        description="Download from a multitude of sites in mp3, flac, wav, or ogg audio; or download as an mp4 file. The supported sites are listed at https://ytdl-org.github.io/youtube-dl/supportedsites.html",
        brief="Download from a list of sites as mp3 or mp4"
        )
    async def download(self, ctx, YTVID, format='mp3'):
        await ctx.send('Ok. Downloading...')
        YTVID2 = YTVID.split("&")
        YTVID = YTVID2[0]
        # changes directory to correct directory
        os.chdir("I:\\Dannybot\\cogs\\cache")
        try:
            if format == "mp4":
                # Runs Youtube-dl command locally with YTVID as a string
                os.system('"youtube-dl -o "ytdl.%(ext)s" -r 999M --no-playlist -f "' +
                          str(format) + " " + str(YTVID))
            elif format == "mp3" or format == "flac" or format == "wav" or format == "ogg":
                # Runs Youtube-dl command locally with YTVID as a string
                os.system('"youtube-dl -x -o "ytdl.%(ext)s" -r 999M --audio-format "' +
                          str(format) + " " + str(YTVID))
            else:
                # Locates song.mp3 in mp3 directory and sends it
                await ctx.reply("The format specified is invalid. Please use `mp4, webm` for video, or `mp3, flac, wav, ogg` for audio.")
        except:
            os.chdir('I:\\Dannybot')
        # Locates song.mp3 in mp3 directory and sends it
        await ctx.reply(file=discord.File('ytdl.' + str(format)))
        os.remove('ytdl.' + str(format))
        os.chdir('I:\\Dannybot')

    @commands.command(
        description="Display file counts for key directories in Dannybot",
        brief="Display file counts for key directories in Dannybot"
        )
    async def db(self, ctx):
        # all of these are just counting the files in these folders
        FemboyDBsize = fileCount("I:\\Dannybot\\cogs\\InternalFiles\\femboy")
        FanboyDBsize = fileCount("I:\\Dannybot\\cogs\\InternalFiles\\fanboy")
        MimiDBsize = fileCount("E:\\Anime\\Kemono girls")
        DooterDBsize = fileCount(
            "I:\\Dannybot\\cogs\\InternalFiles\\PizziImages")
        PooterDBsize = fileCount(
            "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages")
        LeffreyDBsize = fileCount("leffrey_images")
        KoishiDBsize = fileCount("E:\\Anime\\Koishi")
        TTSDBsize = fileCount("speakers")
        BurgerDBsize = fileCount("I:\\Dannybot\\cogs\\InternalFiles\\burger")
        VidDBsize = fileCount("C:\\Users\\weebm\\Videos\\Epic")
        ImgDBsize = fileCount("C:\\Users\\weebm\\Pictures")
        GifDBsize = fileCount(
            "C:\\Users\\weebm\\Pictures\\GIFS")
        GlassCupDBsize = fileCount(
            "I:\\Dannybot\\cogs\\InternalFiles\\glasscup")
        NekoparaDBsize = fileCount("E:\\Anime\\Nekopara")
        # counting ends on this line
        KFDBsize = fileCount("E:\\Anime\\Kemono Friends")

        embed = discord.Embed(title="Dannybot File Totals",
                              color=0xf77e9a)  # define an embed
        # i may want to add these back once he is split into private and public. the same goes for every ommited field here
        embed.add_field(name="Pizzi AI Image Files:",
                        value=DooterDBsize, inline=True)
        embed.add_field(name="Public File Repository:",
                        value=PooterDBsize, inline=True)
        embed.add_field(name="Leffrey Files:",
                        value=LeffreyDBsize, inline=True)
        embed.add_field(name="TTS Speaker Files:",
                        value=TTSDBsize, inline=True)
        embed.add_field(name="Femboy Files:", value=FemboyDBsize, inline=True)
        embed.add_field(name="Fanboy Files:", value=FanboyDBsize, inline=True)
        embed.add_field(name="Video Files:", value=VidDBsize, inline=True)
        embed.add_field(name="Image Files:", value=ImgDBsize, inline=True)
        embed.add_field(name="GIF Files:", value=GifDBsize, inline=True)
        embed.add_field(name="Glass Cup Images:",
                        value=GlassCupDBsize, inline=True)
        embed.add_field(name="Koishi Images:",
                        value=KoishiDBsize, inline=True)
        embed.add_field(name="Burger Files:", value=BurgerDBsize, inline=True)
        embed.add_field(name="Nekopara Files:",
                        value=NekoparaDBsize, inline=True)
        embed.add_field(name="Animal Girl Images:",
                        value=MimiDBsize, inline=True)
        embed.add_field(name="Kemono Friends Files:",
                        value=KFDBsize, inline=True)

        await ctx.reply(embed=embed, mention_author=True)  # send the embed

async def setup(client):
    await client.add_cog(Misc(client))

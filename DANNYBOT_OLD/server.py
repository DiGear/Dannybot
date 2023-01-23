import asyncio
import base64
import datetime
import hashlib
import json
import os
import random
import re
import shutil
import sys
import textwrap
import time
import typing
import urllib
import urllib.request
from collections import namedtuple
from csv import writer
from datetime import datetime
from hashlib import sha512

import aiohttp
import desktopmagic
import discord
import GPUtil
import html2text
import imageio
import openai
import picopt
import PIL
import psutil
import pyautogui
import regex
import requests
import wmi
from bs4 import BeautifulSoup
from discord import File, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from gpuinfo import GPUInfo
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from wand.display import display as mag_display
from wand.image import Image as magick

from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')


class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: server")

    @commands.command(hidden=True)
    async def dooter(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        whitelist = [305161653463285780, 343224184110841856]
        if not ctx.author.id in whitelist:
            await ctx.send("You are not whitelisted for this command!", delete_after=3)
            return
        else:
            if(File_Url == "File_Is_Attachment"):
                Link_To_File = ctx.message.attachments[0].url
            else:
                Link_To_File = File_Url
            await ctx.send("Downloading...", delete_after=3)

            # this code block writes the image data to a file
            with open("I:\\Dannybot\\cogs\\InternalFiles\\PizziImages\\Dooter.png", 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            os.rename("I:\\Dannybot\\cogs\\InternalFiles\\PizziImages\\Dooter.png", "I:\\Dannybot\\cogs\\InternalFiles\\PizziImages\\" +
                      hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest() + ".png")
            await ctx.send("File Downloaded!", delete_after=3)

    @commands.command(
        aliases=['poo'],
        description="Send or recieve a file from a user-built archive of files. You can upload 9 files at a time, or not attach any files to view the archive instead.",
        brief="Send/Recieve files from a public archive."
    )
    async def pooter(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        blacklist = [0]
        downloads = 1
        if ctx.author.id in blacklist:
            await ctx.send("You are blacklisted for this command!", delete_after=10)
            return
        else:
            try:
                if(File_Url == "File_Is_Attachment"):
                    for i in ctx.message.attachments:
                        Link_To_File = i.url
                        # pooter was here
                        await ctx.send("Downloading... (" + str(downloads) + " of " + str(len(ctx.message.attachments))+")", delete_after=3)
                        print(i)
                        downloads += 1
                        with open("I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\Dooter.png", 'wb') as f:
                            f.write(requests.get(Link_To_File).content)
                            f.close
                        os.rename("I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\Dooter.png", "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\" +
                                  hashlib.sha256(str(random.getrandbits(128)).encode('utf-8')).hexdigest() + "." + str(i.url[-5:]).replace('/', ''))
                        await self.client.get_channel(971178342550216705).send(str(ctx.author.name) + " " + str(ctx.author.id) + " has pootered " + str(Link_To_File))
                else:
                    Link_To_File = File_Url

                    await ctx.send("Downloading... (1 of 1)", delete_after=3)
                    with open("I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\Dooter.png", 'wb') as f:
                        f.write(requests.get(Link_To_File).content)
                        f.close
                    os.rename("I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\Dooter.png", "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages\\" +
                              hashlib.sha256(str(random.getrandbits(128)).encode('utf-8')).hexdigest() + "." + str(File_Url[-5:]).replace('/', ''))
                try:
                    with open("I:\\Dannybot\\temp", 'wb') as f:
                        f.write(requests.get(Link_To_File).content)
                        f.close
                except:
                    dir = "I:\\Dannybot\\cogs\\InternalFiles\\PublicImages"
                    file_name = random.choice(os.listdir(dir))
                    with open(f'{dir}\\{file_name}', 'rb') as f:
                        try:
                            await ctx.reply(file=File(f, file_name), mention_author=True)
                            f.close
                            print("sent file: " + file_name)
                            return
                        except:
                            print("attempted to send file larger than limit")
                            return
            except:
                await ctx.send("Error: Catastrophic Failure", delete_after=10)

    @commands.command(
        description="Send a Kemono Friends character from my personal collection.",
        brief="Send a picture of a chosen character from Kemono Friends"
    )
    async def friend(self, ctx, *frien):
        aru2 = badregexcode("Kemofure", frien)
        # set the directory to the result of the regex folder comparison
        dir = 'E:\\Anime\\Kemono Friends\\' + aru2
        # define file_name as an image from the directory
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            f2 = discord.File(f, filename=file_name)
            # count the amount of files in the directory
            friendcount = str(
                len(os.listdir('E:\\Anime\Kemono Friends\\' + aru2)))
            embed = discord.Embed(title="Image of " + aru2, color=0xffc7ed,
                                  description="")  # generate embed
            embed.set_image(url="attachment://"+str(file_name))
            embed.set_footer(text="Found " + friendcount +
                             " results for " + aru2)
            # send embed
            await ctx.reply(file=f2, embed=embed, mention_author=True)

    # literally the exact same code as the above command, different starting directory
    @commands.command(
        description="Send a Nekopara character from my personal collection.",
        brief="Send a picture of a chosen character from Nekopara"
    )
    async def nekopara(self, ctx, *frien):
        aru2 = badregexcode("Nekopara", frien)
        dir = "E:\\Anime\\Nekopara\\" + aru2
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            f2 = discord.File(f, filename=file_name)
            friendcount = str(len(os.listdir("E:\\Anime\\Nekopara\\" + aru2)))
            embed = discord.Embed(color=0xffc7ed)
            embed.set_image(url="attachment://"+str(file_name))
            await ctx.reply(file=f2, embed=embed, mention_author=True)

    @commands.command(
        aliases=['catgirl'],
        description="Send a picture of an catgirl using the nekos.life API.",
        brief="Send a picture of an catgirl"
    )
    async def neko(self, ctx):
        with requests.Session() as s:
            api_output = s.get("https://nekos.life/api/v2/img/neko")
        output = api_output.text
        x = json.loads(output, object_hook=lambda d: namedtuple(
            'X', d.keys())(*d.values()))
        url = x.url
        await ctx.reply(url, mention_author=True)
        print("sent neko from server")

    @commands.command(
        description="Send a video from my personal collection.",
        brief="Send a video from my camera roll"
    )
    async def vid(self, ctx):
        dir = "C:\\Users\\weebm\\Videos\\Epic"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            try:
                await ctx.reply(file=File(f, file_name), mention_author=True)
                f.close
                print("sent file: " + file_name)
            except:
                print("attempted to send file larger than limit")

    @commands.command(
        description="Send a picture from my personal collection.",
        brief="Send a picture from my camera roll"
    )
    async def img(self, ctx):
        dir = "C:\\Users\\weebm\\Pictures"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            try:
                await ctx.reply(file=File(f, file_name), mention_author=True)
                f.close
                print("sent file: " + file_name)
            except:
                print("attempted to send file larger than limit")

    @commands.command(
        description="Send a picture of an animal girl.",
        brief="Send a picture of an animal girl"
    )
    async def mimi(self, ctx):
        dir = "E:\\Anime\\Kemono girls"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            try:
                await ctx.reply(file=File(f, file_name), mention_author=True)
                f.close
                print("sent file: " + file_name)
            except:
                print("attempted to send file larger than limit")

    @commands.command(
        description="Send a picture of Leffrey.",
        brief="Send a picture of Leffrey"
    )
    async def leffrey(self, ctx):
        dir = "I:\\Dannybot\\leffrey_images"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            print("sent file: " + file_name)

    @commands.command(
        description="Send a GIF file.",
        brief="Send a GIF file"
    )
    async def gif(self, ctx):
        dir = "C:\\Users\\weebm\\Pictures\Gifs"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            try:
                await ctx.reply(file=File(f, file_name), mention_author=True)
                f.close
                print("sent file: " + file_name)
            except:
                print("attempted to send file larger than limit")

    @commands.command(
        description="Send a picture of a femboy (anime).",
        brief="Send a picture of an anime femboy"
    )
    async def femboy(self, ctx):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\femboy"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'fem.png'), mention_author=True)
            print("sent femb_image: " + file_name)

    @commands.command(
        description="Send a Fanboy and Chum Chum picture.",
        brief="Send a Fanboy and Chum Chum picture"
    )
    async def fanboy(self, ctx):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\fanboy"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'fan.png'), mention_author=True)
            print("sent fanb_image: " + file_name)

    @commands.command(
        description="Send a picture of a glass cup.",
        brief="Send a picture of a glass cup"
    )
    async def glasscupimage(self, ctx):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\glasscup"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'glass.png'), mention_author=True)
            print("sent glasscupimage: " + file_name)

    @commands.command(
        description="Send a picture of Koishi from Touhou.",
        brief="Send a picture of Koishi from Touhou"
    )
    async def koishi(self, ctx):
        dir = "E:\\Anime\\Koishi"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'koishi.png'), mention_author=True)
            print("sent koishi image: " + file_name)

    @commands.command(
        description="Send a picture of a burger.",
        brief="Send a picture of a burger"
    )
    async def burger(self, ctx):
        dir = "I:\\Dannybot\\cogs\\InternalFiles\\burger"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'burger.png'), mention_author=True)
            print("sent burg_image: " + file_name)

async def setup(client):
    await client.add_cog(Server(client))

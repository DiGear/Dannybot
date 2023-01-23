import datetime
import os
import random
import re
import subprocess
import sys
import textwrap
import time
import typing
import urllib
import urllib.request
from asyncio import sleep
from datetime import datetime

import aiohttp
import desktopmagic
import discord
import GPUtil
import imageio
import picopt
import PIL
import psutil
import pyautogui
import regex
import requests
import wmi
from discord import File, User, guild, member, user
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.file import File
from gpuinfo import GPUInfo
from petpetgif import petpet
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from wand.display import display as mag_display
from wand.image import Image as magick

from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')


class Image(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: image")

    @commands.command(
        description="Flips a provided image horizontally.",
        brief="Flips an image horizontally"
    )
    async def mirror(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\mirror.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    im = PIL.Image.open(
                        f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                    im_mirror = ImageOps.mirror(im)
                    im_mirror.save(
                        f'I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()
            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:
            im = PIL.Image.open('I:\\Dannybot\\cogs\\cache\\mirror.png')
            im_mirror = ImageOps.mirror(im)
            im_mirror.save('I:\\Dannybot\\cogs\\cache\\mirrored.png')
            file_name = "I:\\Dannybot\\cogs\\cache\\mirrored.png"
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.png'), mention_author=True)
                f.close

    @commands.command(
        description="Flips a provided image vertically.",
        brief="Flips an image vertically"
    )
    async def flip(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\flip.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    im = PIL.Image.open(
                        f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                    im_mirror = ImageOps.flip(im)
                    im_mirror.save(
                        f'I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()
            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:
            im = PIL.Image.open('I:\\Dannybot\\cogs\\cache\\flip.png')
            im_mirror = ImageOps.flip(im)
            im_mirror.save('I:\\Dannybot\\cogs\\cache\\flipped.png')
            file_name = "I:\\Dannybot\\cogs\\cache\\flipped.png"
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['petthe', 'pet-the', 'pet_the'],
        description="Applies a petting hand gif to the provided image.",
        brief="That funny hand-petting gif that was a popular meme for a bit"
    )
    async def pet(self, ctx, *args):
        # this checks to see if the image is an attachment or a link
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        # this code block writes the image data to a file
        with open(f'I:\\Dannybot\\cogs\\cache\\pet_in.png', 'wb') as f:
            f.write(requests.get(Link_To_File).content)
            f.close
        os.system('cd I:\\Dannybot\\cogs\\cache')
        os.chdir("I:\\Dannybot\\cogs\\cache")
        petpet.make('pet_in.png', 'pet_the.gif')
        with open(f'pet_the.gif', 'rb') as f:  # prepare the file for sending
            await ctx.reply(file=File(f, 'pet_the.gif'))  # send the file
        f.close  # close the file
        os.chdir('I:\\Dannybot')

    @commands.command(
        aliases=['distort', 'magic'],
        description="Applies a liquid rescale effect to the provided image, using the provided value.",
        brief="Recreation of NotSoBots 'magik' command"
    )
    async def magik(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\distin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    with magick(filename=f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame) as img:
                        img.liquid_rescale(
                            width=int(img.width * 0.5),
                            height=int(img.height * 0.5),
                            rigidity=0
                        )
                        img.liquid_rescale(
                            width=int(img.width * 2),
                            height=int(img.height * 2),
                            rigidity=0
                        )
                        img.save(
                            filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'magik.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:  # still
            with magick(filename="I:\\Dannybot\\cogs\\cache\\distin.png") as img:
                img.liquid_rescale(
                    width=int(img.width * 0.5),
                    height=int(img.height * 0.5),
                    rigidity=0
                )
                img.liquid_rescale(
                    width=int(img.width * 2),
                    height=int(img.height * 2),
                    rigidity=0
                )
                img.save(
                    filename="I:\\Dannybot\\cogs\\cache\\distout.png")
            with open(f'I:\\Dannybot\\cogs\\cache\\distout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'magik.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['df'],
        description="'Deepfries' the provided image.",
        brief="'Deepfries' an image"
    )
    async def deepfry(self, ctx, *args):

        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in Link_To_File:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\shittin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close

        if '.gif' in Link_To_File:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    img = PIL.Image.open(
                        'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame).convert('RGB')
                    img.save('I:\\Dannybot\\cogs\\cache\\GIF\\shittify\\' +
                             frame[-3:]+".jpg", quality=3)
                    sleep(0.3)
                    os.rename('I:\\Dannybot\\cogs\\cache\\GIF\\shittify\\' +
                              frame[-3:]+".jpg", 'I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".jpg")
                    sleep(0.3)
                    with magick(filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".jpg") as img:
                        img.level(0.2, 0.9, gamma=1.1)
                        img.level(0.2, 0.9, gamma=1.1)
                        img.sharpen(radius=8, sigma=4)
                        img.noise("laplacian", attenuate=1.0)
                        img.level(0.2, 0.9, gamma=1.1)
                        img.sharpen(radius=8, sigma=4)
                        img.save(
                            filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".jpg")
            repack_gif_shittify()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'deepfry.gif'), mention_author=True)
                cleanup_gif()
                f.close

        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\dfin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            image = PIL.Image.open(
                'I:\\Dannybot\\cogs\\cache\\dfin.png').convert('RGB')
            image.save("I:\\Dannybot\\cogs\\cache\\dftojpg.jpg", quality=15)
            with magick(filename='I:\\Dannybot\\cogs\\cache\\dftojpg.jpg') as img:
                img.level(0.2, 0.9, gamma=1.1)
                img.level(0.2, 0.9, gamma=1.1)
                img.sharpen(radius=8, sigma=4)
                img.noise("laplacian", attenuate=1.0)
                img.level(0.2, 0.9, gamma=1.1)
                img.sharpen(radius=8, sigma=4)
                img.save(filename='I:\\Dannybot\\cogs\\cache\\dfout.png')
            with open(f'I:\\Dannybot\\cogs\\cache\\dfout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'df.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['shittify', 'jpeg'],
        description="Turns a provided image into a low quality jpeg.",
        brief="Turns an image into a low quality jpeg"
    )
    async def jpg(self, ctx, *args):

        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in Link_To_File:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\shittin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close

        if '.gif' in Link_To_File:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    img = PIL.Image.open(
                        'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame).convert('RGB')
                    img.save('I:\\Dannybot\\cogs\\cache\\GIF\\shittify\\' +
                             frame[-3:]+".jpg", quality=3)
                    sleep(0.3)
                    os.rename('I:\\Dannybot\\cogs\\cache\\GIF\\shittify\\' +
                              frame[-3:]+".jpg", 'I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".jpg")
            repack_gif_shittify()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'shit.gif'), mention_author=True)
                cleanup_gif()
                f.close

        else:  # still
            image = PIL.Image.open(
                'I:\\Dannybot\\cogs\\cache\\shittin.png').convert('RGB')
            image.save("I:\\Dannybot\\cogs\\cache\\shit.jpg", quality=3)
            with open(f'I:\\Dannybot\\cogs\\cache\\shit.jpg', 'rb') as f:
                await ctx.reply(file=File(f, 'shit.jpg'), mention_author=True)
                f.close

    @commands.command(
        aliases=['oatmeal'],
        description="Makes an image super pixelated. The name(s) of the command are in reference to Vinesauce Joel.",
        brief="Makes an image super pixelated"
    )
    async def koala(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\koala_in.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    image = PIL.Image.open(
                        'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                    koala1 = image.resize(
                        (round(image.size[0]*0.07), round(image.size[1]*0.07)), Image.NEAREST)
                    koala1.save('I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                    image = PIL.Image.open(
                        'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                    koala2 = image.resize(
                        (round(image.size[0]*9.6835), round(image.size[1]*9.72)), Image.NEAREST)
                    koala2.save(
                        'I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.gif'), mention_author=True)
                cleanup_gif()
                f.close

        else:
            image = PIL.Image.open('I:\\Dannybot\\cogs\\cache\\koala_in.png')
            koala1 = image.resize(
                (round(image.size[0]*0.07), round(image.size[1]*0.07)), Image.NEAREST)
            koala1.save('I:\\Dannybot\\cogs\\cache\\koala_small.png')
            image = PIL.Image.open(
                'I:\\Dannybot\\cogs\\cache\\koala_small.png')
            koala2 = image.resize(
                (round(image.size[0]*9.6835), round(image.size[1]*9.72)), Image.NEAREST)
            koala2.save('I:\\Dannybot\\cogs\\cache\\koala.png')
            # prepare the file for sending
            with open(f'I:\\Dannybot\\cogs\\cache\\koala.png', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['bulge'],
        description="Applies a bulge effect to a provided image by a specified amount. The default value is 0.5",
        brief="Fisheye an image by a specified amount"
    )
    async def explode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\expin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    with magick(filename=f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame) as img:
                        try:
                            img.implode(amount=-float(Effect_Value))
                        except:
                            img.implode(amount=-float(0.5))  # default value
                        img.save(
                            filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'explode.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:  # still
            with magick(filename='I:\\Dannybot\\cogs\\cache\\expin.png') as img:
                try:
                    img.implode(amount=-float(Effect_Value))
                except:
                    img.implode(amount=-float(0.5))  # default value

                img.save(filename="I:\\Dannybot\\cogs\\cache\\exploded.png")
            with open(f'I:\\Dannybot\\cogs\\cache\\exploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'exploded.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['pinch'],
        description="Applies a pinch effect to a provided image by a specified amount. The default value is 0.5",
        brief="Reverse fisheye an image by a specified amount"
    )
    async def implode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\impin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    with magick(filename=f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame) as img:
                        try:
                            img.implode(amount=float(Effect_Value))
                        except:
                            img.implode(amount=float(0.5))  # default value
                        img.save(
                            filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'implode.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:  # still
            with magick(filename='I:\\Dannybot\\cogs\\cache\\impin.png') as img:
                try:
                    img.implode(amount=float(Effect_Value))
                except:
                    img.implode(amount=float(0.5))  # default value

                img.save(filename="I:\\Dannybot\\cogs\\cache\\imploded.png")
            with open(f'I:\\Dannybot\\cogs\\cache\\imploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'imploded.png'), mention_author=True)
                f.close

    @commands.command(
        description="Applies a set amount of radial blur to a provided image.",
        brief="Applies radial blur to an image"
    )
    async def radial(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]

        if '.gif' in Link_To_File:  # animated
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
        else:  # still
            with open(f'I:\\Dannybot\\cogs\\cache\\radin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close

        if '.gif' in Link_To_File:  # animated
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:
                    with magick(filename=f'I:\\Dannybot\\cogs\\cache\\GIF\\'+frame) as img:
                        img.rotational_blur(angle=6)
                        img.save(
                            filename='I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
            repack_gif()

            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'radial.gif'), mention_author=True)
                cleanup_gif()
                f.close

        else:  # still
            with magick(filename='I:\\Dannybot\\cogs\\cache\\radin.png') as img:
                img.rotational_blur(angle=6)
                img.save(filename="I:\\Dannybot\\cogs\\cache\\radout.png")
            with open(f'I:\\Dannybot\\cogs\\cache\\radout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'radial_blur.png'), mention_author=True)
                f.close

    @commands.command(
        description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext",
        brief="Turns an image into an impact font meme"
    )
    async def meme(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        with open(f'I:\\Dannybot\\cogs\\cache\memein.png', 'wb') as f:
            try:
                f.write(requests.get(context).content)
                f.close
            except:
                if ctx.message.attachments:
                    meme_text_Fallback_Value = context
                    meme_text = context + " " + meme_text
                    if ("ValueError" in meme_text):
                        meme_text = meme_text_Fallback_Value
                    context = ctx.message.attachments[0].url
                    f.write(requests.get(context).content)
                    f.close
                else:
                    meme_text_Fallback_Value = context
                    meme_text = context + " " + meme_text
                    if ("ValueError" in meme_text):
                        meme_text = meme_text_Fallback_Value
                    context = await message_history_img_handler(ctx)
                    f.write(requests.get(context).content)
                    f.close
        try:
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0]
            Bottom_Text = meme_text_splitted[1]
        except:
            Top_Text = meme_text
            Bottom_Text = ""
        Top_Text = Top_Text.upper()
        Bottom_Text = Bottom_Text.upper()
        png_path = ("I:\\Dannybot\\cogs\\cache\memein.png")
        gif_path = None
        is_gif = None
        print("Top_Text is: [" + Top_Text + "]")
        print("Bottom_Text is: [" + Bottom_Text + "]")

        if '.gif' in context:
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(context).content)
                f.close
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
        if '.gif' not in context:
            is_gif = False
            make_meme(Top_Text, Bottom_Text, png_path, is_gif)
        else:
            is_gif = True
            make_meme(Top_Text, Bottom_Text, png_path, is_gif)
        if (is_gif):
            with open(f'I:\\Dannybot\\cogs\\cache\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'meme.gif'), mention_author=True)
                cleanup_gif()
                f.close
        else:
            with open(f'I:\\Dannybot\\cogs\\cache\memeout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'meme.png'), mention_author=True)
                f.close

    @commands.command(
        description="Turn a provided image into a demotivational poster using the syntax: bigtext|smalltext",
        brief="Turns an image into a demotivational poster"
    )
    async def motivate(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        with open(f'I:\\Dannybot\\cogs\\cache\\motivate.png', 'wb') as f:
            try:  # this assume the image was linked to, and attempts to download the file via the link
                f.write(requests.get(context).content)
                f.close
            except:  # if false
                if ctx.message.attachments:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = ctx.message.attachments[0].url
                    f.write(requests.get(context).content)
                    f.close
                else:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = await message_history_img_handler(ctx)
                    f.write(requests.get(context).content)
                    f.close
        try:
            # split the meme text into top and bottom texts
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0]
            Bottom_Text = meme_text_splitted[1]
        except:  # only the top text is present
            Top_Text = meme_text
            Bottom_Text = ""

        print("Top_Text is: [" + Top_Text + "]")
        print("Bottom_Text is: [" + Bottom_Text + "]")

        os.system('demotivate.py "I:\\\Dannybot\\\cogs\\\cache\\motivate.png" "' +
                  str(Top_Text)+'" "'+str(Bottom_Text)+'"')

        os.remove('I:\\Dannybot\\cogs\\cache\\demotivate.png')
        os.rename('I:\\Dannybot\\demotivate.png',
                  'I:\\Dannybot\\cogs\\cache\\demotivate.png')

        # prepare the file for sending
        with open(f'I:\\Dannybot\\cogs\\cache\\demotivate.png', 'rb') as f:
            await ctx.reply(file=File(f, 'meme.png'), mention_author=True)
            f.close
        


    @commands.command(
        description="Command to caption memes in the same way websites like ifunny do, where it puts a white box at the top of the image with black caption text.",
        brief="White box; black text caption an image"
    )
    async def caption(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        with open(f'I:\\Dannybot\\cogs\\cache\memein.png', 'wb') as f:
            try:  # this assume the image was linked to, and attempts to download the file via the link
                f.write(requests.get(context).content)
                f.close
            except:  # if false
                if ctx.message.attachments:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = ctx.message.attachments[0].url
                    f.write(requests.get(context).content)
                    f.close
                else:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = await message_history_img_handler(ctx)
                    f.write(requests.get(context).content)
                    f.close

# massive shitshow for processing GIF files
        if '.gif' in context:
            with open(f'I:\\Dannybot\\cogs\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(context).content)
                f.close
            # convert the gif for frames for processing
            unpack_gif('I:\\Dannybot\\cogs\\cache\\gif.gif')
            for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
                if '.png' in frame:  # otherwise it will see the output folder as a frame and fuck up

                    # run the image manip code in this block
                    os.system('python -m dankcli "I:\\Dannybot\\cogs\\cache\\GIF\\'+frame +
                              '" "{}"  --filename "I:\\Dannybot\\cogs\\cache\\GIF\\output\\'.format(meme_text)+frame+'"')

            repack_gif()  # turn the frames back into a gif while keeping it under 8mb

            # prepare the file for sending
            with open(f'I:\\Dannybot\\cogs\\cache\\outgif.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.gif'), mention_author=True)
                cleanup_gif()  # delete the temporary files made from the unpacking and repacking of gifs
                f.close

        else:
            os.system(
                'python -m dankcli "I:\\Dannybot\\cogs\\cache\\memein.png" "{}"  --filename "I:\\Dannybot\\cogs\\cache\\memeout"'.format(meme_text))
            # prepare the file for sending
            with open(f'I:\\Dannybot\\cogs\\cache\memeout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.png'), mention_author=True)
                f.close

    @commands.command(
        aliases=['pngify', 'transparent'],
        description="Runs the provided image through a (free) API call to remove.bg, to make the image transparent.",
        brief="Remove the background from an image using AI"
    )
    async def removebg(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Removing background. Please wait...", delete_after=5)
        with open(f'I:\\Dannybot\\cogs\\cache\\removebgtemp.png', 'wb') as f:
            f.write(requests.get(Link_To_File).content)
            f.close

        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            data={"image_url": str(Link_To_File), "size": "auto"},
            headers={"X-Api-Key": os.getenv("REMOVEBG_KEY1")},
        )

        if response.status_code == requests.codes.ok:
            with open('I:\\Dannybot\\cogs\\cache\\removed.png', 'wb') as out:
                out.write(response.content)
                f.close
            with open(f'I:\\Dannybot\\cogs\\cache\\removed.png', 'rb') as f:
                await ctx.reply(file=File(f, 'removed.png'), mention_author=True)
                f.close
        else:
            await ctx.reply("Processing of the image failed. This is most likely because no background was detected.", mention_author=True)
            print(response.content)


async def setup(client):
    await client.add_cog(Image(client))

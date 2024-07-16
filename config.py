# this is where most of the bullshit will be taking place
# anything you need to configure will be located in here

# ----------
# Imports
# ----------

import asyncio
import base64
import glob
import hashlib
import io
import json
import logging
import math
import shutil
import os
import random
import re
import subprocess
import colorsys
import string
import sys
import textwrap
import threading
import time
import typing
import urllib
import urllib.request
import uuid
from collections import namedtuple, deque
from datetime import datetime
from functools import lru_cache, partial
from io import BytesIO
from pathlib import Path
from textwrap import wrap
from typing import Literal
from io import StringIO

# tensorfuck
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from textgenrnn import textgenrnn
from urllib import request
from rembg import new_session, remove
from xml.etree import ElementTree

import aiofiles
import aiohttp
import discord
import furl
import numpy
import openai
import PIL
import requests
import ujson
import websocket
import traceback
import warnings
import yt_dlp
from aiohttp import ClientSession
from colorama import init, Fore
from discord import File, Interaction, InteractionType, app_commands, FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from petpetgif import petpet
from PIL import (
    GifImagePlugin,
    Image,
    ImageColor,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
    ImageSequence,
)
from wand.image import Image as magick

load_dotenv()
logger = logging.getLogger(__name__)

# ----------
# Variables
# (im considering moving these into a large config json, not the functions but just this stuff)
# ----------

# dannybot config
dannybot_prefixes = {"d.", "#", "D.", "ratio + "}  # bot prefix(es)
dannybot_token = os.getenv("TOKEN")  # token
dannybot_team_ids = {343224184110841856, 158418656861093888, 249411048518451200}
dannybot_denialRatio = 250  # chance for dannybot to deny your command input
dannybot_denialResponses = {
    "no",
    "nah",
    "nope",
    "no thanks",
}  # what dannybot says upon denial
dannybot = (
    os.getcwd()
)  # easy to call variable that stores our current working directory
cache_clear_onLaunch = True  # dannybot will clear his cache on launch if set to true
clean_pooter_onLaunch = True  # dannybot will clean up pooter on launch if set to true
database_acceptedFiles = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "mp4",
    "webm",
    "mov",
}  # list of accepted files for the bots public database
cmd_blacklist = ["0"]  # Users who cant use the bot lol
whitelist = {
    779136383033147403,
    367767486004985857,
    706353387855151105,
    922428724744454164,
    796606820348723230,
    1131490848014598268,
    352972878645428225,
}  # servers with full bot access

# configs for the image manipulation commands
imageLower = 250  # the smallest image width image commands will use. if the image is thinner than this, it will proportionally scale to this size
imageUpper = 1500  # the largest image width image commands will use. if the image is wider than this, it will proportionally scale to this size

# channel configs (WHY WERE THESE NEVER PUT INTO THE .ENV UNTIL 2023/4/5)
bookmarks_channel = int(os.getenv("BOOKMARKS"))  # channel to send personal bookmarks to
logs_channel = int(os.getenv("LOGS"))  # channel to log commands

# more .env keys being assigned here
openai.api_key = os.getenv("OPENAI_API_KEY")  # i hope i can remove this soon
tenor_apikey = os.getenv("TENOR_KEY")
AlphaVantageAPI = os.getenv("AV_API_KEY")

# internal paths
Cookies = f"{dannybot}\\assets\\cookies.txt"  # set this to your YT-DL cookies
Waifu2x = f"{dannybot}\\tools\\waifu2x-caffe\\waifu2x-caffe-cui.exe"  # set this to the path of your waifu2x-caffe-cui.exe file in your waifu2x-caffe install

# 8ball responses for the 8ball command
ball_responses = {
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
    "Very doubtful.",
    "yeah",
    "nah",
}

# logo list for the logo command
logolist = {
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
}

# this is for the undertext command
deltarune_dw = {
    "ralsei",
    "lancer",
    "king",
    "jevil",
    "queen",
    "spamton",
    "clyde",
    "lori",
    "rhombo",
}


# ----------
# Functions
# ----------


# Custom colors
def custom_color_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, Warning):
        msg = Fore.YELLOW + f"Warning: {exc_type.__name__}: {exc_value}\n" + Fore.RESET
    else:
        error_msg = f"Error: {exc_value}\n"
        traceback_str = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )
        msg = Fore.RED + error_msg + traceback_str + Fore.RESET
    sys.stderr.write(msg)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = custom_color_handler
warnings.showwarning = custom_color_handler


# take a provided gif file and unpack each frame to /cache/ffmpegs
def unpack_gif(file, id=None):
    print(Fore.LIGHTMAGENTA_EX + "unpacking gif..." + Fore.RESET)
    directory = f"cache/ffmpeg/{id}" if id is not None else "cache/ffmpeg"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f'ffmpeg -i "{file}" -vf fps=25 -vsync 0 "{directory}/temp%04d.png" -y')
    return


# take each frame in /cache/ffmpeg/out and turn it back into a gif
def repack_gif(id=None):
    if id is not None:
        directory = f"cache/ffmpeg/output/{id}"
    else:
        directory = f"cache/ffmpeg/output"

    palette_path = f"{directory}/palette.png"
    output_gif = f"cache/ffmpeg_out{id}.gif"
    print(Fore.LIGHTMAGENTA_EX + "generating palette..." + Fore.RESET)
    os.system(
        f'ffmpeg -i "{directory}/temp%04d.png" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" {palette_path} -y'
    )
    print(Fore.LIGHTMAGENTA_EX + "repacking gif..." + Fore.RESET)
    os.system(
        f'ffmpeg -i "{directory}/temp%04d.png" -i "{palette_path}" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 99M "{output_gif}" -y'
    )
    shutil.rmtree(directory)
    print(Fore.LIGHTMAGENTA_EX + f"Deleted directory {directory}" + Fore.RESET)

    return


def repack_gif_JPG(id=None):
    if id is not None:
        directory = f"cache/ffmpeg/output/{id}"
    else:
        directory = f"cache/ffmpeg/output"

    palette_path = f"{directory}/palette.png"
    output_gif = "cache/ffmpeg_out.gif"
    print(Fore.LIGHTMAGENTA_EX + "generating palette..." + Fore.RESET)
    os.system(
        f'ffmpeg -i "{directory}/temp%04d.png.jpg" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" {palette_path} -y'
    )
    print(Fore.LIGHTMAGENTA_EX + "repacking gif (jpg)..." + Fore.RESET)
    os.system(
        f'ffmpeg -i "{directory}/temp%04d.png.jpg" -i "{palette_path}" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 99M "{output_gif}" -y'
    )
    shutil.rmtree(directory)
    print(Fore.LIGHTMAGENTA_EX + f"Deleted directory {directory}" + Fore.RESET)
    return


def generate_id():
    return random.randint(15679, 48568696543)


# generate a random hexadecimal string
def randhex(bits):
    num_bytes = (bits + 3) // 4
    random_number = random.getrandbits(bits)
    random_hex = hex(random_number)[2:].zfill(num_bytes)
    return random_hex


# clear the cache folder of all files
def clear_cache():
    cache_folder = Path(f"{dannybot}/cache")
    ffmpeg_cache_folder = cache_folder / "ffmpeg"
    output_folder = ffmpeg_cache_folder / "output"

    def clear_files(folder):
        for file_path in folder.glob("*"):
            if file_path.is_file() and "git" not in str(file_path):
                try:
                    os.remove(file_path)
                    print(
                        Fore.LIGHTMAGENTA_EX + f"Deleted file: {file_path}" + Fore.RESET
                    )
                except PermissionError:
                    print(
                        Fore.YELLOW
                        + f"Skipped file: {file_path} (File in use)"
                        + Fore.RESET
                    )
                    continue
            elif file_path.is_dir() and file_path != output_folder:
                try:
                    for sub_file in file_path.glob("**/*"):
                        if sub_file.is_file():
                            os.remove(sub_file)
                            print(
                                Fore.LIGHTMAGENTA_EX
                                + f"Deleted file: {sub_file}"
                                + Fore.RESET
                            )
                    os.rmdir(file_path)
                    print(
                        Fore.LIGHTMAGENTA_EX
                        + f"Deleted folder: {file_path}"
                        + Fore.RESET
                    )
                except OSError:
                    print(
                        Fore.YELLOW
                        + f"Skipped folder: {file_path} (Not empty or in use)"
                        + Fore.RESET
                    )
                    continue

    thread = threading.Thread(target=clear_files, args=(ffmpeg_cache_folder,))
    thread.start()
    thread.join()

    print(Fore.BLUE + "Cache cleared." + Fore.RESET)

# get the amount of files in a folder
def fileCount(folder):
    return sum(len(filenames) for _, _, filenames in os.walk(folder))


# checks if a value is a float, why the fuck is this an external function
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# get the total size of all files in a folder
def fileSize(folder):
    total_size = 0
    for root, _, filenames in os.walk(folder, topdown=False):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            total_size += os.path.getsize(file_path)

    units = ["bytes", "KB", "MB", "GB", "TB"]
    unit_index = min(len(units) - 1, int(math.floor(math.log(total_size, 1024))))
    total_size /= 1024**unit_index

    return f"{total_size:.2f} {units[unit_index]}"


def undertext(name, text, isAnimated):
    # animated override: if the name contains "animated-", remove it and set isAnimated to True
    if text.endswith("True"):
        text = text[:-4]
        isAnimated = True

    # AU style overrides: if the name contains a valid AU, add the AU style to the name and text
    if "uf" in name:  # underfell
        name = f"{name}&boxcolor=b93b3c&asterisk=b93b3c&charcolor=b93b3c"
        text = f"color=%23b93b3c%20{text}"
    if name in deltarune_dw:  # deltarune
        name = f"{name}&box=deltarune&mode=darkworld"

    # character overrides: replace underscores with dashes, then use the dictionary to replace the name with the link
    character_links = {
        "danny": "https://cdn.discordapp.com/attachments/560608550850789377/1005989141768585276/dannyportrait1.png",
        "danny-funny": "https://cdn.discordapp.com/attachments/560608550850789377/1005999509496660060/dannyportrait3.png",
        "danny-angry": "https://cdn.discordapp.com/attachments/560608550850789377/1005989142825553971/dannyportrait4.png",
        "danny-pissed": "https://cdn.discordapp.com/attachments/560608550850789377/1005989142083145828/dannyportrait2.png",
        "crackhead": "https://cdn.discordapp.com/attachments/1063552619110477844/1076067803649556480/image.png",
        "pizzi": "https://cdn.discordapp.com/attachments/1063552619110477844/1082228005256044575/pizziportrait1.png",
        "pizzi-stare": "https://cdn.discordapp.com/attachments/1063552619110477844/1082228014856814612/pizziportrait2.png",
        "pizzi-scream": "https://cdn.discordapp.com/attachments/1063552619110477844/1082228022796615720/pizziportrait3.png",
        "sam": "https://cdn.discordapp.com/attachments/1063552619110477844/1082220603387428894/samportrait1.png",
        "flashlight": "https://cdn.discordapp.com/attachments/1063552619110477844/1068251386430619758/image.png",
        "ezo": "https://cdn.discordapp.com/attachments/1063552619110477844/1068251386430619758/image.png",
        "ezogaming": "https://cdn.discordapp.com/attachments/1063552619110477844/1068251386430619758/image.png",
        "incine": "https://cdn.discordapp.com/attachments/1063552619110477844/1063552737435992084/FIncine.png",
        "cris": "https://cdn.discordapp.com/attachments/1063552619110477844/1063552816397951037/FCris.png",
        "seki": "https://cdn.discordapp.com/attachments/1063552619110477844/1063738177212399658/sekiportrait1.png",
        "seki-eyes": "https://cdn.discordapp.com/attachments/560608550850789377/1075684786489798696/sekiportrait2.png",
        "seki-evil": "https://cdn.discordapp.com/attachments/1063552619110477844/1075687740793946122/sekiportrait3.png",
        "leffrey": "https://cdn.discordapp.com/attachments/886788323648094219/1068253912919982100/image.png",
        "reimu-fumo": "https://cdn.discordapp.com/attachments/1063552619110477844/1082233613040504892/image.png",
        "suggagugga": "https://cdn.discordapp.com/attachments/1063552619110477844/1068248384164614154/mcflurger.png",
    }

    name = character_links.get(name, name)

    # link overrides: if the name starts with "https://", add "custom&url=" to the beginning of the name
    if name.startswith("http"):
        name = f"custom&url={name}"

    # text overrides: modify the box and text display based on passed parameters
    if "font=wingdings" in text:
        name = f"{name}&asterisk=null"

    # finalizing: set the name and text to the name and text, then return the name, text, and isAnimated
    name = name
    # replacing the discord double underscore shit with spaces
    text = text.replace("_ _", "%20")
    return name, text, isAnimated


# grab the gif url of a tenor id using the tenor api
def gettenor(gifid=None):
    # get the api key from the config file
    apikey = tenor_apikey
    r = requests.get(
        "https://api.tenor.com/v1/gifs?ids=%s&key=%s&media_filter=minimal"
        % (gifid, apikey)
    )

    if r.status_code == 200:
        gifs = ujson.loads(r.content)
    else:
        gifs = None
    return gifs["results"][0]["media"][0]["gif"]["url"]


# this shit hole of a function is how dannybot handles files sent within discord and how they should be used with other args
async def resolve_args(ctx, args, attachments, type="image"):
    url = None
    tenor = False
    avatar = False
    text = " ".join(args)
    print(Fore.LIGHTMAGENTA_EX + "Resolving URL and arguments..." + Fore.RESET)

    extensions = {
        "image": ("png", "jpg", "jpeg", "gif", "bmp", "webp"),
        "audio": ("wav", "ogg", "mp3", "flac", "aiff", "opus", "m4a", "oga"),
        "midi": ("mid", "midi", "smf"),
        "video": ("mp4", "avi", "mpeg", "mpg", "webm", "mov", "mkv"),
        "3d": ("obj", "fbx", "stl", "dae"),
        "office": ("doc", "docx", "xls", "xlsx", "ppt", "pptx"),
        "text": ("txt", "rtf", "json"),
        "code": ("py", "java", "cpp", "c", "h", "html", "css", "js", "php", "cs", "rb"),
    }
    extension_list = [ext.lower() for ext in extensions.get(type, ())]

    # Helper function to ensure proper URL combination
    def combine_url(url_parts):
        return "?".join(filter(None, url_parts))

    # Grab a URL if the command is a reply to an image
    if ctx.message.reference:
        referenced_message = await ctx.fetch_message(ctx.message.reference.message_id)
        if "https://tenor.com/view/" in referenced_message.content and type == "image":
            tenor = True
            tenor_id = re.search(
                r"tenor\.com/view/.*-(\d+)", referenced_message.content
            ).group(1)
            url = gettenor(tenor_id)
            print(Fore.BLUE + f"URL from Tenor: {url}" + Fore.RESET)
        elif referenced_message.attachments:
            for attachment in referenced_message.attachments:
                if attachment.content_type.startswith(type):
                    url_parts = attachment.url.split("?")
                    url = combine_url(url_parts)
                    print(Fore.BLUE + f"URL from reply: {url}" + Fore.RESET)
                    break
        else:
            http_urls = re.findall(r"http\S+", referenced_message.content)
            if http_urls:
                http_url_parts = http_urls[0].split("?")
                ext = http_url_parts[0].split(".")[-1]
                if ext.lower() in extension_list:
                    url = combine_url(http_url_parts)
                    print(Fore.BLUE + f"URL from reply: {url}" + Fore.RESET)

    # Grab a URL if the command has an attachment
    if not url and attachments:
        for attachment in attachments:
            if attachment.content_type.startswith(type):
                url_parts = attachment.url.split("?")
                url = combine_url(url_parts)
                print(Fore.BLUE + f"URL from attachment: {url}" + Fore.RESET)
                break

    # Grab a URL passed from args
    if not url:
        if args and args[0].startswith("http"):
            if "https://tenor.com/view/" in args[0]:
                tenor = True
                tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", args[0]).group(1)
                url = gettenor(tenor_id)
                print(Fore.BLUE + f"URL from Tenor: {url}" + Fore.RESET)
            else:
                url_parts = args[0].split("?")
                url = combine_url(url_parts)
                text = " ".join(args[1:])
                print(Fore.BLUE + f"URL from argument: {url}" + Fore.RESET)

        # Grab a URL from mentioned user's avatar
        if ctx.message.mentions:
            mentioned_member = ctx.message.mentions[0]

            if mentioned_member.guild_avatar:
                url = str(mentioned_member.guild_avatar.url)
                print(
                    Fore.BLUE + f"URL from avatar of mentioned user: {url}" + Fore.RESET
                )
                avatar = True
            else:
                url = str(mentioned_member.avatar.url)
                print(
                    Fore.BLUE + f"URL from avatar of mentioned user: {url}" + Fore.RESET
                )
                avatar = True

    # Message content iteration
    if not url:
        channel = ctx.message.channel
        async for msg in channel.history(limit=500):
            content = msg.content

            # Grab the URL from the last sent message's attachment
            for attachment in msg.attachments:
                attch_url_parts = attachment.url.split("?")
                ext = attch_url_parts[0].split(".")[-1]
                if ext.lower() in extension_list:
                    url = combine_url(attch_url_parts)
                    print(Fore.BLUE + f"URL from attachment: {url}" + Fore.RESET)
                    break
            if url:
                break

            # Grab the URL (tenor) from the last sent message
            if "https://tenor.com/view/" in content and type == "image":
                tenor = True
                tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", content).group(1)
                url = gettenor(tenor_id)
                print(Fore.BLUE + f"URL from Tenor: {url}" + Fore.RESET)
                break

            # Grab the URL from the last sent message
            if type == "image":
                http_urls = re.findall(r"http\S+", content)
                if http_urls:
                    http_url_parts = http_urls[0].split("?")
                    ext = http_url_parts[0].split(".")[-1]
                    if ext.lower() in extension_list:
                        url = combine_url(http_url_parts)
                        print(
                            Fore.BLUE + f"URL from message content: {url}" + Fore.RESET
                        )
                        break

            # Generic URL extraction
            http_urls = re.findall(r"http\S+", content)
            if http_urls:
                http_url_parts = http_urls[0].split("?")[0]
                ext = http_url_parts.split(".")[-1]
                if ext.lower() in extension_list:
                    url = combine_url(http_url_parts)
                    print(Fore.BLUE + f"URL from message content: {url}" + Fore.RESET)
                    break

    try:
        if not avatar and isinstance(url, list):
            url = combine_url(url)
        text = re.sub(r"<@[^>]+>\s*", "", text)
    except Exception as e:
        # Handle any exceptions in URL processing
        print(Fore.RED + f"Error combining URL: {e}" + Fore.RESET)
    finally:
        print(Fore.CYAN + f"Arguments: {url}, {text}" + Fore.RESET)
        return [url, text]


# change hue (apparently not an inbuilt function of PIL)
def change_hue(img, target_hue):
    img = img.convert(
        "RGB"
    )  # Ensure image is RGB (so that i can convert it to hsv lmfao)
    new_pixels = []

    for r, g, b in img.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h = (h + target_hue) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        new_pixels.append((int(r * 255), int(g * 255), int(b * 255)))

    img.putdata(new_pixels)
    return img


# deepfry an image
def deepfry(inputpath, outputpath):
    # open image
    image = PIL.Image.open(f"{inputpath}").convert("RGB")
    image.save(f"{dannybot}\\cache\\deepfry_in.jpg", quality=15)
    with magick(filename=f"{dannybot}\\cache\\deepfry_in.jpg") as img:
        for _ in range(2):
            img.level(0.2, 0.9, gamma=1.1)
            img.sharpen(radius=8, sigma=4)
        img.noise("laplacian")
        img.save(filename=outputpath)
    return


# resize image to fit within bounds
def imagebounds(path):
    # Open image and get size
    image = PIL.Image.open(path)
    width, height = image.size

    # Calculate the aspect ratio
    aspect_ratio = height / width

    # Check if image width is smaller than the lower bound
    if width < imageLower:
        new_width = imageLower
        new_height = int(new_width * aspect_ratio)
    # Check if image width is larger than the upper bound
    elif width > imageUpper:
        new_width = imageUpper
        new_height = int(new_width * aspect_ratio)
    else:
        # No need to resize the image
        return

    # Resize the image and save it
    resized_image = image.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)
    resized_image.save(path)


# primary function of the meme command
def make_meme(Top_Text, Bottom_Text, path):
    # Open the image
    img = PIL.Image.open(path)

    # Calculate the image bounds
    imagebounds(path)

    # Open the image and convert it to RGBA format
    img = PIL.Image.open(path)
    img = img.convert("RGBA")

    # Set the path to the font file
    font_path = f"{dannybot}\\assets\\impactjpn.otf"

    # Set the padding size
    padding = 10

    # Split the top and bottom text into if lengths exceed 27 characters (this should ultimately end us up with 3 lines of text)
    top_text_lines = [Top_Text]
    bottom_text_lines = [Bottom_Text]

    if len(Top_Text) > 27:
        top_text_lines = textwrap.wrap(Top_Text, width=27)

    if len(Bottom_Text) > 27:
        bottom_text_lines = textwrap.wrap(Bottom_Text, width=27)
        bottom_text_lines.reverse()

    # Create a new image with transparent background for text overlay
    text_image = PIL.Image.new("RGBA", img.size, (255, 255, 255, 0))
    text_draw = PIL.ImageDraw.Draw(text_image)

    # Calculate the font size for the top text
    max_top_font_size = int(img.width / 8)
    top_font_size = max_top_font_size

    # Adjust the font size until the top text fits within the image width
    while True:
        top_line_widths = [
            text_draw.textsize(
                line, font=PIL.ImageFont.truetype(font_path, top_font_size)
            )[0]
            for line in top_text_lines
        ]
        if max(top_line_widths) <= img.width - padding * 2:
            break
        top_font_size -= 1

    # Calculate the font size for the bottom text
    max_bottom_font_size = int(img.width / 8)
    bottom_font_size = max_bottom_font_size

    # Adjust the font size until the bottom text fits within the image width
    while True:
        bottom_line_widths = [
            text_draw.textsize(
                line, font=PIL.ImageFont.truetype(font_path, bottom_font_size)
            )[0]
            for line in bottom_text_lines
        ]
        if max(bottom_line_widths) <= img.width - padding * 2:
            break
        bottom_font_size -= 1

    # Set the initial height for the top text
    top_text_height = 0

    # Draw each line of the top text on the image
    for line, font_size in zip(top_text_lines, [top_font_size] * 3):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_width, text_height = text_draw.textsize(line, font=font)
        x = (img.width - text_width) // 2
        y = padding + top_text_height
        text_draw.text(
            (x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black"
        )
        top_text_height += text_height

    # Set the initial height for the bottom text
    bottom_text_height = 0

    # Draw each line of the bottom text on the image
    for line, font_size in zip(bottom_text_lines, [bottom_font_size] * 3):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_width, text_height = text_draw.textsize(line, font=font)
        x = (img.width - text_width) // 2
        y = img.height - padding - text_height - bottom_text_height
        text_draw.text(
            (x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black"
        )
        bottom_text_height += text_height

    # Combine the original image with the text overlay
    composite_image = PIL.Image.alpha_composite(img, text_image)

    # Set the output path for the final meme image
    output_path = f"{dannybot}\\cache\\meme_out.png"

    # Save the composite image as the final meme image
    composite_image.save(output_path)
    return


# gif version
def make_meme_gif(Top_Text, Bottom_Text):
    # iterate through every frame in the ffmpeg folder and edit them
    for frame in os.listdir(f"{cache_dir}\\ffmpeg"):
        if ".png" in frame:
            # open image in PIL
            img = PIL.Image.open(f"{dannybot}\\cache\\ffmpeg\\{frame}")
            path = f"{dannybot}\\cache\\ffmpeg\\{frame}"

            # Calculate the image bounds
            imagebounds(path)

            # Open the image and convert it to RGBA format
            img = PIL.Image.open(path)
            img = img.convert("RGBA")

            # Set the path to the font file
            font_path = f"{dannybot}\\assets\\impactjpn.otf"

            # Set the padding size
            padding = 10

            # Split the top and bottom text into if lengths exceed 27 characters (this should ultimately end us up with 3 lines of text)
            top_text_lines = [Top_Text]
            bottom_text_lines = [Bottom_Text]

            if len(Top_Text) > 27:
                top_text_lines = textwrap.wrap(Top_Text, width=27)

            if len(Bottom_Text) > 27:
                bottom_text_lines = textwrap.wrap(Bottom_Text, width=27)
                bottom_text_lines.reverse()

            # Create a new image with transparent background for text overlay
            text_image = PIL.Image.new("RGBA", img.size, (255, 255, 255, 0))
            text_draw = PIL.ImageDraw.Draw(text_image)

            # Calculate the font size for the top text
            max_top_font_size = int(img.width / 8)
            top_font_size = max_top_font_size

            # Adjust the font size until the top text fits within the image width
            while True:
                top_line_widths = [
                    text_draw.textsize(
                        line, font=PIL.ImageFont.truetype(font_path, top_font_size)
                    )[0]
                    for line in top_text_lines
                ]
                if max(top_line_widths) <= img.width - padding * 2:
                    break
                top_font_size -= 1

            # Calculate the font size for the bottom text
            max_bottom_font_size = int(img.width / 8)
            bottom_font_size = max_bottom_font_size

            # Adjust the font size until the bottom text fits within the image width
            while True:
                bottom_line_widths = [
                    text_draw.textsize(
                        line, font=PIL.ImageFont.truetype(font_path, bottom_font_size)
                    )[0]
                    for line in bottom_text_lines
                ]
                if max(bottom_line_widths) <= img.width - padding * 2:
                    break
                bottom_font_size -= 1

            # Set the initial height for the top text
            top_text_height = 0

            # Draw each line of the top text on the image
            for line, font_size in zip(top_text_lines, [top_font_size] * 3):
                font = PIL.ImageFont.truetype(font_path, font_size)
                text_width, text_height = text_draw.textsize(line, font=font)
                x = (img.width - text_width) // 2
                y = padding + top_text_height
                text_draw.text(
                    (x, y),
                    line,
                    font=font,
                    fill="white",
                    stroke_width=2,
                    stroke_fill="black",
                )
                top_text_height += text_height

            # Set the initial height for the bottom text
            bottom_text_height = 0

            # Draw each line of the bottom text on the image
            for line, font_size in zip(bottom_text_lines, [bottom_font_size] * 3):
                font = PIL.ImageFont.truetype(font_path, font_size)
                text_width, text_height = text_draw.textsize(line, font=font)
                x = (img.width - text_width) // 2
                y = img.height - padding - text_height - bottom_text_height
                text_draw.text(
                    (x, y),
                    line,
                    font=font,
                    fill="white",
                    stroke_width=2,
                    stroke_fill="black",
                )
                bottom_text_height += text_height

            # Combine the original image with the text overlay
            composite_image = PIL.Image.alpha_composite(img, text_image)

            # save the resulting image
            output_path = f"{dannybot}\\cache\\ffmpeg\\output\\{frame}"
            composite_image.save(output_path)
    repack_gif()

    return


# for caption stuff
def wrap_text(text, draw, font, max_width):
    wrapped_lines = []
    for line in text.split("\n"):
        if draw.textsize(line, font=font)[0] <= max_width:
            wrapped_lines.append(line)
        else:
            words = line.split(" ")
            wrapped_line = ""
            for word in words:
                test_line = f"{wrapped_line} {word}".strip()
                if draw.textsize(test_line, font=font)[0] <= max_width:
                    wrapped_line = test_line
                else:
                    wrapped_lines.append(wrapped_line)
                    wrapped_line = word
            wrapped_lines.append(wrapped_line)
    return wrapped_lines


# makes a filename only have valid windows file chars
def sanitize_filename(filename):
    valid_chars = string.ascii_letters + string.digits + "._- "
    sanitized_filename = "".join(char for char in filename if char in valid_chars)
    return sanitized_filename


# generate list from directory of files
def listgen(directory):
    list = os.listdir(directory)
    string = ", ".join(list)
    return string


# i hate this - FDG
# i went back and make this more annoying to read and look at so hopefully people avoid it and dont get infected with the uwu virus
def uwuify(input_text):
    def case_agnostic_replace(text, old, new):
        result = ""
        i = 0
        while i < len(text):
            if text[i : i + len(old)].lower() == old.lower():
                result += text[i : i + len(old)].replace(old, new, 1)
                i += len(old)
            else:
                result += text[i]
                i += 1
        return result

    modified_text1 = case_agnostic_replace(input_text, "l", "w")
    modified_text2 = case_agnostic_replace(modified_text1, "u", "uu")
    modified_text3 = case_agnostic_replace(modified_text2, "r", "w")
    modified_text4 = case_agnostic_replace(modified_text3, "the", "de")
    modified_text5 = case_agnostic_replace(modified_text4, "to", "tu")
    emoticons = ["^_^", ">w<", "x3", "^.^", "^-^", "(・ˋω´・)", "x3", ";;w;;"]
    words = modified_text5.split()
    output_text = []
    for i, word in enumerate(words):
        output_text.append(word)
        if i < len(words) - 1 and random.random() < 0.1:
            output_text.append(random.choice(emoticons))
    modified_text6 = " ".join(output_text)
    modified_text7 = case_agnostic_replace(modified_text6, "~", "")
    modified_text = case_agnostic_replace(modified_text7, "!", " !~ ")
    return modified_text


# clean up the pooter folder
def clean_pooter():
    directory_path = os.path.join(dannybot, "database", "Pooter")

    if not os.path.exists(directory_path):
        logging.error(Fore.RED + "Pooter folder not found. Aborting." + Fore.RESET)
        return

    file_hashes = {}
    lock = threading.Lock()

    def calculate_file_hash(file_path, block_size=65536):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(block_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def clean_file(file):
        nonlocal file_hashes
        file_path = os.path.join(directory_path, file)
        if "." not in file:
            os.remove(file_path)
            with lock:
                print(Fore.LIGHTMAGENTA_EX + f"Deleted: {file}" + Fore.RESET)
            return
        file_hash = calculate_file_hash(file_path)
        with lock:
            if file_hash in file_hashes:
                os.remove(file_path)
                print(Fore.LIGHTMAGENTA_EX + f"Deleted: {file}" + Fore.RESET)
            else:
                file_hashes[file_hash] = file_path

    files_to_clean = [
        file
        for file in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, file))
    ]

    threads = []
    for file in files_to_clean:
        thread = threading.Thread(target=clean_file, args=(file,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(Fore.BLUE + "No more files to clean." + Fore.RESET)

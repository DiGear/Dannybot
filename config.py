# this is where most of the bullshit will be taking place
# anything you need to configure will be located in here
# -------------------------------------------------------
# Imports
# -------------------------------------------------------

# Standard library imports
import asyncio
import base64
import builtins
import glob
import hashlib
import io
import json
import logging
import math
import os
import random
import re
import shutil
import string
import subprocess
import sys
import textwrap
import threading
import time
import traceback
import typing
import uuid
import urllib
import webbrowser
from collections import deque, namedtuple
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache, partial
from io import BytesIO, StringIO
from pathlib import Path
from textwrap import wrap
from typing import Literal
from urllib import request
from xml.etree import ElementTree

# Third-party imports
import aiofiles
import aiohttp
import discord
import furl
import gradio as gr
import numpy
import openai
import PIL
import pydub
import requests
import ujson
import websocket
import yt_dlp
from aiohttp import ClientSession
from colorama import Fore, init
from discord import (
    AppCommandContext,
    FFmpegPCMAudio,
    File,
    Interaction,
    InteractionType,
    app_commands,
)
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
from pydub import AudioSegment
from rembg import new_session, remove
from thefuzz import fuzz
from wand.image import Image as magick

load_dotenv()  # load extra private variables from dotenv
logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Classes
# -------------------------------------------------------


# this allows me to manage "bags" of values for random selection without repeats
class BagRandom:
    def __init__(self, file_name):
        self.bags = {}
        self.default_bag = None
        self.directory = "bags"
        self.file_path = os.path.join(self.directory, file_name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.load_bags()

    def create_bag(self, name, values):
        """Create a new bag with a given name and values."""
        self.bags[name] = {"original_values": list(values), "bag": list(values)}
        if self.default_bag is None:
            self.default_bag = name
        self.save_bags()

    def set_bag(self, name):
        """Set the default bag to use."""
        if name in self.bags:
            self.default_bag = name

    def _refill_bag(self, name):
        """Refill the specified bag if empty."""
        if name in self.bags:
            self.bags[name]["bag"] = list(self.bags[name]["original_values"])
        self.save_bags()

    def choice(self, name):
        """Return a random element from the specified bag."""
        if name not in self.bags:
            raise ValueError(f"Bag '{name}' does not exist.")

        bag = self.bags[name]
        if not bag["bag"]:
            self._refill_bag(name)
        choice = random.choice(bag["bag"])
        bag["bag"].remove(choice)
        self.save_bags()
        return choice

    def add_values(self, name, values):
        """Add values to the specified bag."""
        if name in self.bags:
            self.bags[name]["original_values"].extend(values)
            self.bags[name]["bag"].extend(values)
        else:
            raise ValueError(f"Bag '{name}' does not exist.")
        self.save_bags()

    def save_bags(self):
        """Save the current state of the bags to a JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(self.bags, file, indent=4)

    def load_bags(self):
        """Load the bags from a JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.bags = json.load(file)
        else:
            self.bags = {}


# -------------------------------------------------------
# Variables
# -------------------------------------------------------

dannybot_prefixes = {"d.", "#", "D.", "ratio + "}  # bot prefix(es)
dannybot_token = os.getenv("TOKEN")  # token
dannybot_team_ids = {343224184110841856, 158418656861093888, 249411048518451200}
dannybot_denialRatio = 250  # chance for dannybot to deny your command input
dannybot_denialResponses = [  # responses that dannybot can use when denying a command
    "no",
    "nah",
    "nope",
    "no thanks",
]
dannybot = os.getcwd()  # current working directory of dannybot for ease of access

cache_clear_onLaunch = True  # dannybot will clear his cache on launch if set to true
clean_pooter_onLaunch = True  # dannybot will clean up pooter on launch if set to true

# accepted file extensions for pooter
database_acceptedFiles = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "mp4",
    "webm",
    "mov",
    # lazy caps
    "PNG",
    "JPG",
    "JPEG",
    "GIF",
    "WEBP",
    "MP4",
    "WEBM",
    "MOV",
}

# whitelist of server IDs that have full bot access
whitelist = {
    779136383033147403,
    367767486004985857,
    706353387855151105,
    922428724744454164,
    796606820348723230,
    1131490848014598268,
    352972878645428225,
    1274900393285124126,
    882143616754147350,
}

# minimum and maximum image widths to use for processing
imageLower = 250  # the smallest image width image commands will use
imageUpper = 1500  # the largest image width image commands will use

bookmarks_channel = int(os.getenv("BOOKMARKS"))  # channel to send personal bookmarks to
logs_channel = int(os.getenv("LOGS"))  # channel to log commands

openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API key
tenor_apikey = os.getenv("TENOR_KEY")  # Tenor API key for GIFs
AlphaVantageAPI = os.getenv("AV_API_KEY")  # Alpha Vantage API key for stock data

Cookies = f"{dannybot}\\assets\\cookies.txt"  # set this to your YT-DL cookies
Waifu2x = f"{dannybot}\\tools\\waifu2x-caffe\\waifu2x-caffe-cui.exe"  # path to waifu2x-caffe-cui.exe

# responses for the 8ball command
ball_responses = [
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
]

# list of logo types for the logo command
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

# list for the undertext command featuring Deltarune characters
deltarune_dw = [
    "ralsei",
    "lancer",
    "king",
    "jevil",
    "queen",
    "spamton",
    "clyde",
    "lori",
    "rhombo",
]

# -------------------------------------------------------
# Functions
# -------------------------------------------------------


# private helper to unify repack_gif and repack_gif_JPG
def _repack_gif_core(
    directory,
    input_pattern,
    palette_path,
    output_gif,
    palette_msg,
    repack_msg,
    remove_directory=False,
):
    print(Fore.LIGHTMAGENTA_EX + palette_msg + Fore.RESET)
    # generate a palette from the input frames using ffmpeg
    os.system(
        f'ffmpeg -i "{directory}/{input_pattern}" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" {palette_path} -y'
    )
    print(Fore.LIGHTMAGENTA_EX + repack_msg + Fore.RESET)
    # repack the frames into a GIF using the generated palette
    os.system(
        f'ffmpeg -i "{directory}/{input_pattern}" -i "{palette_path}" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 99M "{output_gif}" -y'
    )

    if remove_directory:
        shutil.rmtree(directory)
    print(Fore.LIGHTMAGENTA_EX + f"Deleted directory {directory}" + Fore.RESET)
    return


# private helper to unify repeated meme text logic
def _draw_meme_text(img, Top_Text, Bottom_Text, font_path):
    # create a transparent image for drawing text overlays
    text_image = PIL.Image.new("RGBA", img.size, (255, 255, 255, 0))
    text_draw = PIL.ImageDraw.Draw(text_image)
    padding = 10  # padding

    # wrap text if it exceeds a certain length
    def get_wrapped_lines(text_value):
        if len(text_value) > 27:
            return textwrap.wrap(text_value, width=27)
        return [text_value]

    top_text_lines = get_wrapped_lines(Top_Text)
    bottom_text_lines = get_wrapped_lines(Bottom_Text)
    bottom_text_lines.reverse()  # reverse bottom text lines for proper drawing order

    # determine maximum font sizes based on image width
    max_top_font_size = int(img.width / 8)
    top_font_size = max_top_font_size
    # reduce font size until text fits within image width
    while True:
        top_line_widths = [
            text_draw.textbbox(
                (0, 0), line, font=PIL.ImageFont.truetype(font_path, top_font_size)
            )[2]
            for line in top_text_lines
        ]
        if max(top_line_widths) <= img.width - padding * 2:
            break
        top_font_size -= 1

    max_bottom_font_size = int(img.width / 8)
    bottom_font_size = max_bottom_font_size
    # reduce font size until text fits within image width
    while True:
        bottom_line_widths = [
            text_draw.textbbox(
                (0, 0), line, font=PIL.ImageFont.truetype(font_path, bottom_font_size)
            )[2]
            for line in bottom_text_lines
        ]
        if max(bottom_line_widths) <= img.width - padding * 2:
            break
        bottom_font_size -= 1

    # draw the top text lines onto the image
    top_text_height = 0
    for line, font_size in zip(top_text_lines, [top_font_size] * len(top_text_lines)):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_bbox = text_draw.textbbox((0, 0), line, font=font)  # Get the bounding box
        text_width, text_height = (
            text_bbox[2],
            text_bbox[3],
        )  # Extract width and height from bbox
        x = (img.width - text_width) // 2  # center horizontally
        y = padding + top_text_height
        text_draw.text(
            (x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black"
        )
        top_text_height += text_height

    bottom_text_height = 0
    for line, font_size in zip(
        bottom_text_lines, [bottom_font_size] * len(bottom_text_lines)
    ):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_bbox = text_draw.textbbox((0, 0), line, font=font)  # Get the bounding box
        text_width, text_height = (
            text_bbox[2],
            text_bbox[3],
        )  # Extract width and height from bbox
        x = (img.width - text_width) // 2  # center horizontally
        y = img.height - padding - text_height - bottom_text_height
        text_draw.text(
            (x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black"
        )
        bottom_text_height += text_height

    # composite the text overlay with the original image
    return PIL.Image.alpha_composite(img, text_image)


# take a provided gif file and unpack each frame to /cache/ffmpegs
def unpack_gif(file, id=None):
    print(Fore.LIGHTMAGENTA_EX + f"unpacking gif {id}..." + Fore.RESET)
    directory = f"cache/ffmpeg/{id}" if id is not None else "cache/ffmpeg"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # use ffmpeg to extract frames from the gif
    os.system(f'ffmpeg -i "{file}" -vf fps=25 -vsync 0 "{directory}/temp%04d.png" -y')
    return


# take each frame in /cache/ffmpeg/out and turn it back into a gif
def repack_gif(id=None):
    if id is not None:
        directory = f"cache/ffmpeg/output/{id}"
    else:
        directory = f"cache/ffmpeg/output"
    if not os.path.exists(directory):
        os.makedirs(directory)

    palette_path = f"{directory}/palette.png"
    output_gif = (
        f"cache/ffmpeg_out{id}.gif" if id is not None else f"cache/ffmpeg_out.gif"
    )
    # call the helper function to generate the palette and repack the gif
    _repack_gif_core(
        directory=directory,
        input_pattern="temp%04d.png",
        palette_path=palette_path,
        output_gif=output_gif,
        palette_msg="generating palette...",
        repack_msg="repacking gif...",
        remove_directory=False,
    )


# the same thing but jpg
def repack_gif_JPG(id=None):
    if id is not None:
        directory = f"cache/ffmpeg/output/{id}"
    else:
        directory = f"cache/ffmpeg/output"
    if not os.path.exists(directory):
        os.makedirs(directory)

    palette_path = f"{directory}/palette.png"
    output_gif = "cache/ffmpeg_out.gif"
    _repack_gif_core(
        directory=directory,
        input_pattern="temp%04d.png.jpg",
        palette_path=palette_path,
        output_gif=output_gif,
        palette_msg="generating palette...",
        repack_msg="repacking gif (jpg)...",
        remove_directory=True,
    )


# generate a random numerical id within a given range
def generate_id():
    return random.randint(15679, 48568696543)


# generate a random hexadecimal string with a specified number of bits
def randhex(bits):
    num_bytes = (bits + 3) // 4
    random_number = random.getrandbits(bits)
    random_hex = hex(random_number)[2:].zfill(num_bytes)
    return random_hex


# clear the cache folder of all files
def clear_cache():
    # define the cache folder and ffmpeg subfolder paths
    cache_folder = Path(f"{dannybot}/cache")
    ffmpeg_cache_folder = cache_folder / "ffmpeg"
    folders_to_clear = [cache_folder, ffmpeg_cache_folder]

    def clear_files(folder):
        # iterate through all files and delete them if possible
        for file_path in folder.rglob("*"):
            if file_path.is_file() and "git" not in str(file_path):
                try:
                    os.remove(file_path)
                    print(Fore.LIGHTMAGENTA_EX + f"Deleted: {file_path}" + Fore.RESET)
                except PermissionError:
                    print(
                        Fore.YELLOW + f"Skipped: {file_path} (File in use)" + Fore.RESET
                    )
                    continue
        # iterate through directories and delete them
        for dir_path in folder.rglob("*"):
            if dir_path.is_dir() and "git" not in str(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(
                        Fore.LIGHTMAGENTA_EX
                        + f"Deleted folder: {dir_path}"
                        + Fore.RESET
                    )
                except PermissionError:
                    print(
                        Fore.YELLOW
                        + f"Skipped: {dir_path} (Folder in use)"
                        + Fore.RESET
                    )
                    continue

    threads = []
    # create threads for clearing each folder concurrently
    for folder in folders_to_clear:
        thread = threading.Thread(target=clear_files, args=(folder,))
        thread.start()
        threads.append(thread)

    # wait for all threads to complete
    for thread in threads:
        thread.join()

    print(Fore.BLUE + "Cache cleared." + Fore.RESET)


# get the total count of files in a folder
def fileCount(folder):
    return sum(len(filenames) for _, _, filenames in os.walk(folder))


# check if a given value can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# calculate the total size of all files within a folder
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


# undertext bullshit
def undertext(name, text, isAnimated):
    # replace underscores with dashes
    name = name.replace("_", "-")

    # handle animation override
    if text.endswith("True"):
        text = text[:-4]
        isAnimated = True

    # dict that maps shorthand names to demirramon names
    character_links = {
        "danny": "digear/danny",
        "danny-funny": "digear/danny-funny",
        "danny-angry": "digear/danny-angry",
        "danny-pissed": "digear/danny-pissed",
        "crackhead": "digear/crackhead",
        "pizzi": "digear/pizzi",
        "pizzi-stare": "digear/pizzi-stare",
        "pizzi-screech": "digear/pizzi-screech",
        "sam": "digear/sam",
        "ezogaming": "flashlight/ezo",
        "seki": "digear/seki",
        "seki-eyes": "digear/seki-eyes",
        "seki-evil": "digear/seki-evil",
        "leffrey": "digear/leffrey",
        "reimu-fumo": "digear/reimu-fumo",
        "suggagugga": "digear/suggagugga",
    }

    name = character_links.get(name, name)

    # define AU styles for alternate text styling
    au_styles = {"uf": "&boxcolor=b93b3c&asterisk=b93b3c&charcolor=b93b3c"}

    # apply AU styles
    for au, style in au_styles.items():
        if au in name:
            name += style
            text = f"color=%23b93b3c%20{text}"
            break

    # append Deltarune styles
    name += "&box=deltarune&mode=darkworld" if name in deltarune_dw else ""

    # this makes custom links work
    name = f"custom&url={name}" if name.startswith("http") else name

    # font override
    name += "&asterisk=null" if "font=wingdings" in text else ""

    # discord underscore thing
    text = text.replace("_ _", "%20")

    return name, text, isAnimated


# retrieve the GIF URL from Tenor using a provided Tenor gif ID
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
    # return the URL of the gif from the Tenor response
    return gifs["results"][0]["media"][0]["gif"]["url"]


# dumb stupid bullshit
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

    def combine_url(url_parts):
        return "?".join(filter(None, url_parts))

    # grab a URL if the command is a reply to an image
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

    # grab a URL if the command has an attachment
    if not url and attachments:
        for attachment in attachments:
            if attachment.content_type.startswith(type):
                url_parts = attachment.url.split("?")
                url = combine_url(url_parts)
                print(Fore.BLUE + f"URL from attachment: {url}" + Fore.RESET)
                break

    # grab a URL passed from args
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

        # grab a URL from mentioned user's avatar
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

    # iterate over recent messages to find a valid URL if none was found
    if not url:
        channel = ctx.message.channel
        async for msg in channel.history(limit=500):
            content = msg.content

            # check for attachment URLs in the message
            for attachment in msg.attachments:
                attch_url_parts = attachment.url.split("?")
                ext = attch_url_parts[0].split(".")[-1]
                if ext.lower() in extension_list:
                    url = combine_url(attch_url_parts)
                    print(Fore.BLUE + f"URL from attachment: {url}" + Fore.RESET)
                    break
            if url:
                break

            # check for Tenor URL in message content for image type
            if "https://tenor.com/view/" in content and type == "image":
                tenor = True
                tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", content).group(1)
                url = gettenor(tenor_id)
                print(Fore.BLUE + f"URL from Tenor: {url}" + Fore.RESET)
                break

            # check for generic HTTP URLs in message content
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

            # generic URL extraction code
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
        # remove mentions from the text argument
        text = re.sub(r"<@[^>]+>\s*", "", text)
    except Exception as e:
        print(Fore.RED + f"Error combining URL: {e}" + Fore.RESET)
    finally:
        print(Fore.CYAN + f"Arguments: {url}, {text}" + Fore.RESET)
        return [url, text]


# change the hue of an image by a given shift (in degrees) and adjust saturation
def change_hue(image, hue_shift, saturation_shift=1):
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # split the image into individual bands
    r, g, b, a = image.split()

    # convert the image to HSV
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()

    # normalize hue_shift from degrees (0-360) to the 0-255 scale used by PIL
    hue_shift_normalized = int((hue_shift / 360.0) * 255)

    # adjust hue by adding hue_shift and wrap around using modulo 256
    h = h.point(lambda p: (p + hue_shift_normalized) % 256)

    # adjust saturation ensuring values remain in the valid range (0-255)
    s = s.point(lambda p: min(max(int(p * saturation_shift), 0), 255))

    # merge the adjusted HSV channels and convert back to RGBA
    hsv_image = Image.merge("HSV", (h, s, v))
    rgba_image = hsv_image.convert("RGBA")

    # reattach the original alpha channel
    final_image = Image.merge("RGBA", (*rgba_image.split()[:-1], a))
    return final_image


# funni deepfry
def deepfry(inputpath, outputpath):
    image = PIL.Image.open(f"{inputpath}").convert("RGB")
    image.save(
        f"{dannybot}\\cache\\deepfry_in.jpg", quality=15
    )  # this makes it look like shit
    with magick(
        filename=f"{dannybot}\\cache\\deepfry_in.jpg"
    ) as img:  # this make it shittier
        for _ in range(2):
            img.level(0.2, 0.9, gamma=1.1)
            img.sharpen(radius=8, sigma=4)
        img.noise("laplacian")
        img.save(filename=outputpath)
    return


# resize an image to imagebounds
def imagebounds(path):
    image = PIL.Image.open(path)
    width, height = image.size

    # calculate the aspect ratio to preserve proportions
    aspect_ratio = height / width

    # adjust image size
    if width < imageLower:
        new_width = imageLower
        new_height = int(new_width * aspect_ratio)
    elif width > imageUpper:
        new_width = imageUpper
        new_height = int(new_width * aspect_ratio)
    else:
        return

    resized_image = image.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)
    resized_image.save(path)


# main function for meme text generation
def make_meme(Top_Text, Bottom_Text, path):
    image = PIL.Image.open(path)
    imagebounds(path)

    img = PIL.Image.open(path)
    img = img.convert("RGBA")

    font_path = f"{dannybot}\\assets\\impactjpn.otf"
    composite_image = _draw_meme_text(img, Top_Text, Bottom_Text, font_path)

    output_path = f"{dannybot}\\cache\\meme_out.png"

    composite_image.save(output_path)
    return


# meme generation function for GIFs
def make_meme_gif(Top_Text, Bottom_Text):
    # iterate through each frame extracted by ffmpeg
    for frame in os.listdir(f"{dannybot}\\cache\\ffmpeg"):
        if ".png" in frame:
            img_path = f"{dannybot}\\cache\\ffmpeg\\{frame}"
            imagebounds(img_path)
            img = PIL.Image.open(img_path).convert("RGBA")
            font_path = f"{dannybot}\\assets\\impactjpn.otf"
            composite_image = _draw_meme_text(
                img, Top_Text, Bottom_Text, font_path
            )  # make meme
            output_path = f"{dannybot}\\cache\\ffmpeg\\output\\{frame}"
            composite_image.save(output_path)
    repack_gif()
    return


#  wrap text to a specified maximum width for d.caption
def wrap_text(text, draw, font, max_width):
    wrapped_lines = []
    for line in text.split("\n"):
        text_bbox = draw.textbbox(
            (0, 0), line, font=font
        )  # Get the bounding box for the line
        if text_bbox[2] <= max_width:  # text_bbox[2] gives the width of the line
            wrapped_lines.append(line)
        else:
            words = line.split(" ")
            wrapped_line = ""
            for word in words:
                test_line = f"{wrapped_line} {word}".strip()
                text_bbox_test = draw.textbbox((0, 0), test_line, font=font)
                if (
                    text_bbox_test[2] <= max_width
                ):  # text_bbox_test[2] gives the width of the test line
                    wrapped_line = test_line
                else:
                    wrapped_lines.append(wrapped_line)
                    wrapped_line = word
            wrapped_lines.append(wrapped_line)
    return wrapped_lines


# sanitize a filename by
def sanitize_filename(filename):
    valid_chars = string.ascii_letters + string.digits + "._- "
    sanitized_filename = "".join(char for char in filename if char in valid_chars)
    return sanitized_filename


# generate a comma-separated list of files in a directory
def listgen(directory):
    list = os.listdir(directory)
    string = ", ".join(list)
    return string


# clean up the pooter folder by removing duplicate files or files with no extension
def clean_pooter():
    directory_path = os.path.join(dannybot, "database", "Pooter")

    if not os.path.exists(directory_path):
        logging.error(Fore.RED + "Pooter folder not found. Aborting." + Fore.RESET)
        return

    file_hashes = {}
    lock = threading.Lock()

    # calculate the MD5 hash of a file to detect duplicates
    def calculate_file_hash(file_path, block_size=65536):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(block_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    # process each file and remove if duplicate or lacking an extension
    def clean_file(file):
        nonlocal file_hashes
        file_path = os.path.join(directory_path, file)

        # skip files without an extension and delete them
        if "." not in file:
            os.remove(file_path)
            with lock:
                print(Fore.LIGHTMAGENTA_EX + f"Deleted: {file}" + Fore.RESET)
            return

        # calculate file hash to check for duplicates
        file_hash = calculate_file_hash(file_path)
        with lock:
            if file_hash in file_hashes:
                os.remove(file_path)
                print(Fore.LIGHTMAGENTA_EX + f"Deleted: {file}" + Fore.RESET)
            else:
                file_hashes[file_hash] = file_path

    # get list of files to clean in the pooter folder
    files_to_clean = [
        file
        for file in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, file))
    ]

    max_threads = 25
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(clean_file, files_to_clean)

    print(Fore.BLUE + "No more files to clean." + Fore.RESET)

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
import os
import random
import re
import string
import sys
import textwrap
import time
import traceback
import typing
import urllib
import urllib.request
from collections import namedtuple
from datetime import datetime
from textwrap import wrap
from typing import Literal

import aiofiles
import aiohttp
import discord
import furl
import numpy
import openai
import PIL
import pyttsx3
import requests
from discord import File, app_commands
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from petpetgif import petpet
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)
from wand.image import Image as magick

load_dotenv()
logger = logging.getLogger(__name__)

# ----------
# VariablesZ
# ----------

# dannybot config
dannybot_prefixes = ["d.", "#", "D.", "ratio + "] #bot prefix(es)
dannybot_token = os.getenv("TOKEN") #token
dannybot_team_ids = [343224184110841856, 158418656861093888, 249411048518451200]
dannybot_denialRatio = 250 # chance for dannybot to deny your command input
dannybot_denialResponses = ['no' , 'nah', 'nope', 'no thanks', 'use slashes lol'] # what dannybot says upon denial
dannybot = os.getcwd() # easy to call variable that stores our current working directory
cache_clear_onLaunch = True # dannybot will clear his cache on launch if set to true
database_acceptedFiles = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov'] # list of accepted files for the bots public database

#configs for the image manipulation commands
imageLower = 250 # the smallest image width image commands will use. if the image is thinner than this, it will proportionally scale to this size
imageUpper = 1500 # the largest image width image commands will use. if the image is wider than this, it will proportionally scale to this size

#channel configs (WHY WERE THESE NEVER PUT INTO THE .ENV UNTIL 2023/4/5)
bookmarks_channel = int(os.getenv("BOOKMARKS")) #channel to send personal bookmarks to
logs_channel = int(os.getenv("LOGS")) # channel to log commands

# more .env keys being assigned here
openai.api_key = os.getenv("OPENAI_API_KEY")
removebg_key = os.getenv("REMOVEBG_KEY")
tenor_apikey =  os.getenv("TENOR_KEY")

# external paths
NekoparaPath = "I:\\Anime\\Nekopara" # put your nekopara files into here
MimiPath = "I:\\Anime\\Kemono girls" # put your animal girl files here
PicturesPath = "C:\\Users\\weebm\\Pictures" # set this to your pictures folder
VideosPath = "C:\\Users\\weebm\\Videos\\epic" # set this to your videos folder
GifsPath = "C:\\Users\\weebm\\Pictures\\GIFS" # set this to your gifs folder

# internal paths
Cookies = f"{dannybot}\\assets" # set this to your YT-DL cookies folder
UltimateVocalRemover = f"{dannybot}\\tools\\UltimateVocalRemover" # set this to the path of your install of UltimateVocalRemover
Waifu2x = f"{dannybot}\\tools\\waifu2x-caffe\\waifu2x-caffe-cui.exe" # set this to the path of your waifu2x-caffe-cui.exe file in your waifu2x-caffe install

# 8ball responses for the 8ball command
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
    "Very doubtful."
]

# logo list for the logo command
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

# this is for the undertext command
deltarune_dw = [
    'ralsei',
    'lancer',
    'king', 'jevil',
    'queen',
    'spamton',
    "clyde",
    "lori",
    "rhombo"
]


# dalle shit
DALLE_API = "https://backend.craiyon.com/generate"
DALLE_FORMAT = "png"

# ----------
# Functions
# ----------

# take a provided gif file and unpack each frame to /cache/ffmpegs
def unpack_gif(file):
    logger.info("unpacking gif...")
    os.system(f'ffmpeg -i "{file}" -vf fps=25 -vsync 0 "{dannybot}\\cache\\ffmpeg\\temp%04d.png" -y')
    return

# take each frame in /cache/ffmpeg/out and turn it back into a gif
def repack_gif():
    logger.info("generating palette...")
    os.system(f'ffmpeg -i "{dannybot}\\cache\\ffmpeg\\output\\temp%04d.png" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" {dannybot}\\cache\\ffmpeg\\output\\palette.png -y')
    logger.info("repacking gif...")
    os.system(f'ffmpeg -i "{dannybot}\\cache\\ffmpeg\\output\\temp%04d.png" -i "{dannybot}\\cache\\ffmpeg\\output\\palette.png" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 8M "{dannybot}\\cache\\ffmpeg_out.gif" -y')
    return

# take each frame in /cache/ffmpeg/out and turn it back into a gif (jpg variant)
def repack_gif_JPG():
    logger.info("generating palette...")
    logger.info("repacking gif (jpg)...")
    os.system(f'ffmpeg -i "{dannybot}\\cache\\ffmpeg\\output\\temp%04d.png.jpg" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" {dannybot}\\cache\\ffmpeg\\output\\palette.png -y')
    os.system(f'ffmpeg -i "{dannybot}\\cache\\ffmpeg\\output\\temp%04d.png.jpg" -i "{dannybot}\\cache\\ffmpeg\\output\\palette.png" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 8M "{dannybot}\\cache\\ffmpeg_out.gif" -y')
    return

# clear the ffmpeg and ffmpeg/output folders of any residual files
def cleanup_ffmpeg():
    ffmpeg_folder = f"{dannybot}\\cache\\ffmpeg"
    output_folder = f"{ffmpeg_folder}\\output"

    logger.info("Cleaning up...")

    # Remove residual .png files in ffmpeg folder
    for file_path in glob.glob(f"{ffmpeg_folder}/*.png"):
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")

    # Remove residual .png files in ffmpeg/output folder
    for file_path in glob.glob(f"{output_folder}/*.png"):
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")

# generate a random hexadecimal string
def randhex(bits):
    random_number = random.getrandbits(bits)
    random_bytes = random_number.to_bytes((bits + 7) // 8, 'big')
    random_hex = random_bytes.hex()
    return random_hex

# clear the cache folder of all files
def clear_cache():
    cache_folder = f'{dannybot}\\cache'
    ffmpeg_cache_folder = f'{cache_folder}\\ffmpeg'
    output_folder = f'{ffmpeg_cache_folder}\\output'

    for file_path in glob.glob(f'{cache_folder}/*'):
        if os.path.isfile(file_path) and 'git' not in file_path and '.' in file_path:
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")

    for file_path in glob.glob(f'{ffmpeg_cache_folder}/*.png'):
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")

    for file_path in glob.glob(f'{output_folder}/*.png'):
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"Deleted: {file_path}")
    return

# get the amount of files in a folder
def fileCount(folder):
    return sum(len(filenames) for _, _, filenames in os.walk(folder))

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# get the total size of all files in a folder
def fileSize(folder):   
    total_size = 0

    # Iterate through the directory structure recursively
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)  # Add the size of each file to the total

    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0

    # Convert the total size to the appropriate unit
    while total_size >= 1024 and unit_index < len(units) - 1:
        total_size /= 1024.0
        unit_index += 1

    # Format the result with two decimal places and the corresponding unit label
    return f"{total_size:.2f} {units[unit_index]}"

'''
def ezogaming_regex(datalist, dataentry):
    # Read the file with the list of entries
    with open(f"{dannybot}\\ezogaming\\{datalist}_char") as f:
        entries = [x.rstrip() for x in f.readlines()]

    # Read the file with the list of aliases
    with open(f"{dannybot}\\ezogaming\\{datalist}_checker") as f:
        aliases = [x.rstrip() for x in f.readlines()]

    # Remove all non-alphabetic characters from the input
    input_text = re.sub("[^a-z]", "", " ".join(dataentry[:]).lower())

    # Create a list of indices for the entries
    indices = list(range(len(entries)))

    # Shuffle the indices
    random.shuffle(indices)

    # Iterate through the shuffled indices
    for i in indices:
        # Remove non-alphabetic characters from the entry and its alias
        entry = re.sub("[^a-z]", "", entries[i].lower().strip())
        alias = re.sub("[^a-z]", "", aliases[i].lower().strip())

        # If a match is found between the input and the entry or alias
        if input_text in entry or input_text in alias:
            # Return the matching entry
            return entries[i]

    # If no match is found, return a random entry
    return random.choice(entries)
'''

def undertext(name, text, isAnimated):
    
    # animated override: if the name contains "animated-", remove it and set isAnimated to True
    if text.endswith("True"):
        text = text[:-4]
        isAnimated = True
    
    # AU style overrides: if the name contains a valid AU, add the AU style to the name and text
    if "uf" in name: # underfell
        name = f"{name}&boxcolor=b93b3c&asterisk=b93b3c&charcolor=b93b3c"
        text = f"color=%23b93b3c%20{text}"
    if name in deltarune_dw: # deltarune
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
            "suggagugga": "https://cdn.discordapp.com/attachments/1063552619110477844/1068248384164614154/mcflurger.png"
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
    #replacing the discord double underscore shit with spaces
    text = text.replace("_ _", "%20")
    return name, text, isAnimated

# grab the gif url of a tenor id using the tenor api
def gettenor(gifid=None):
    # get the api key from the config file
    apikey = tenor_apikey
    r = requests.get(
        "https://api.tenor.com/v1/gifs?ids=%s&key=%s&media_filter=minimal" % (gifid, apikey))

    if r.status_code == 200:
        gifs = json.loads(r.content)
    else:
        gifs = None
    return gifs['results'][0]['media'][0]['gif']['url']

async def resolve_args(ctx, args, attachments, type="image"):
    url = None
    text = ' '.join(args)  # Combine all arguments as text
    logger.info("Resolving URL and arguments...")

    extensions = {
        "image": ('png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'),
        "audio": ('wav', 'ogg', 'mp3', 'flac', 'aiff', 'opus', 'm4a', 'oga'),
        "midi": ('mid', 'midi'),
        "video": ('mp4', 'avi', 'mpeg', 'mpg', 'webm', 'mov', 'mkv'),
        "3d": ('obj', 'fbx', 'stl', 'dae'),
        "office": ('doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'),
        "text": ('txt', 'rtf', 'json'),
        "code": ('py', 'java', 'cpp', 'c', 'h', 'html', 'css', 'js', 'php', 'cs', 'rb')
    }
    extension_list = extensions.get(type, ())

    if ctx.message.reference:
        referenced_message = await ctx.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            for attachment in referenced_message.attachments:
                if attachment.content_type.startswith(type):
                    url = attachment.url.split('?')[0]
                    logger.info("URL from reply: %s", url)
                    break

    if not url and attachments:
        # Check if there are attachments
        for attachment in attachments:
            if attachment.content_type.startswith(type):
                url = attachment.url.split('?')[0]
                logger.info("URL from attachment: %s", url)
                break

    if not url:
        # Check if the first argument is a URL
        if args and args[0].startswith('http'):
            url = args[0].split('?')[0]  # Extract the URL
            text = ' '.join(args[1:])
            logger.info("URL from argument: %s", url)

    if not url:
        # Get URL using the message history
        channel = ctx.message.channel

        async for msg in channel.history(limit=500):
            if msg.attachments:
                ext = msg.attachments[0].url.split('.')[-1].lower()
                if ext in extension_list:
                    url = msg.attachments[0].url
                    logger.info("URL from message attachment: %s", url)
                    break

            if type == "image":
                if 'https://tenor.com/view/' in msg.content:
                    match = re.search(r"tenor\.com/view/.*-(\d+)", msg.content)
                    if match:
                        tenor_id = match.group(1)
                        url = str(gettenor(tenor_id))
                        logger.info("URL from Tenor: %s", url)
                        break

                ext = str(msg.content).split('.')[-1].lower()
                if ext in extension_list:
                    urls = re.findall(r"http\S+", msg.content)
                    if urls:
                        url = urls[0].split('?')[0]
                        logger.info("URL from message content: %s", url)
                        break
            else:
                if 'http' in msg.content:
                    ext = str(msg.content).split('.')[-1]
                    if ext in extension_list:
                        urls = re.findall(r"http\S+", msg.content)
                        if urls:
                            url = urls[0].split('?')[0]
                            break

    logger.info(f"Arguments: {text}")

    return [url, text]

# deepfry an image
def deepfry(inputpath, outputpath):
    # open image
    image = PIL.Image.open(f'{inputpath}').convert('RGB')
    image.save(f'{dannybot}\\cache\\deepfry_in.jpg', quality=15)
    with magick(filename=f'{dannybot}\\cache\\deepfry_in.jpg') as img:
        # apply deepfry
        img.level(0.2, 0.9, gamma=1.1)
        img.level(0.2, 0.9, gamma=1.1)
        img.sharpen(radius=8, sigma=4)
        img.noise("laplacian", attenuate=1.0)
        img.level(0.2, 0.9, gamma=1.1)
        img.sharpen(radius=8, sigma=4)
        img.save(filename=f'{outputpath}')
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
    padding = 20

    # Split the top and bottom text into lines if their lengths exceed 40 characters
    top_text_lines = [Top_Text]
    bottom_text_lines = [Bottom_Text]
    if (len(Top_Text) > 40):
        top_text_lines = [Top_Text[:len(Top_Text) // 2], Top_Text[len(Top_Text) // 2:]]
    if (len(Bottom_Text) > 40):
        bottom_text_lines = [Bottom_Text[len(Bottom_Text) // 2:], Bottom_Text[:len(Bottom_Text) // 2]]

    # Create a new image with transparent background for text overlay
    text_image = PIL.Image.new("RGBA", img.size, (255, 255, 255, 0))
    text_draw = PIL.ImageDraw.Draw(text_image)

    # Calculate the font size for the top text
    max_top_font_size = int(img.width / 10)
    top_font_size = max_top_font_size

    # Adjust the font size until the top text fits within the image width
    while True:
        top_line_widths = [text_draw.textsize(line, font=PIL.ImageFont.truetype(font_path, top_font_size))[0] for line in top_text_lines]
        if max(top_line_widths) <= img.width - padding * 2:
            break
        top_font_size -= 1

    # Calculate the font size for the bottom text
    max_bottom_font_size = int(img.width / 10)
    bottom_font_size = max_bottom_font_size

    # Adjust the font size until the bottom text fits within the image width
    while True:
        bottom_line_widths = [text_draw.textsize(line, font=PIL.ImageFont.truetype(font_path, bottom_font_size))[0] for line in bottom_text_lines]
        if max(bottom_line_widths) <= img.width - padding * 2:
            break
        bottom_font_size -= 1

    # Set the initial height for the top text
    top_text_height = 0

    # Draw each line of the top text on the image
    for line, font_size in zip(top_text_lines, [top_font_size, top_font_size]):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_width, text_height = text_draw.textsize(line, font=font)
        x = (img.width - text_width) // 2
        y = padding + top_text_height
        text_draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        top_text_height += text_height

    # Set the initial height for the bottom text
    bottom_text_height = 0

    # Draw each line of the bottom text on the image
    for line, font_size in zip(bottom_text_lines, [bottom_font_size, bottom_font_size]):
        font = PIL.ImageFont.truetype(font_path, font_size)
        text_width, text_height = text_draw.textsize(line, font=font)
        x = (img.width - text_width) // 2
        y = img.height - padding - text_height - bottom_text_height
        text_draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
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
    for frame in os.listdir(f"{dannybot}\\cache\\ffmpeg\\"):
        if '.png' in frame:

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
            padding = 20

            # Split the top and bottom text into lines if their lengths exceed 40 characters
            top_text_lines = [Top_Text]
            bottom_text_lines = [Bottom_Text]
            if (len(Top_Text) > 40):
                top_text_lines = [Top_Text[:len(Top_Text) // 2], Top_Text[len(Top_Text) // 2:]]
            if (len(Bottom_Text) > 40):
                bottom_text_lines = [Bottom_Text[len(Bottom_Text) // 2:], Bottom_Text[:len(Bottom_Text) // 2]]

            # Create a new image with transparent background for text overlay
            text_image = PIL.Image.new("RGBA", img.size, (255, 255, 255, 0))
            text_draw = PIL.ImageDraw.Draw(text_image)

            # Calculate the font size for the top text
            max_top_font_size = int(img.width / 10)
            top_font_size = max_top_font_size

            # Adjust the font size until the top text fits within the image width
            while True:
                top_line_widths = [text_draw.textsize(line, font=PIL.ImageFont.truetype(font_path, top_font_size))[0] for line in top_text_lines]
                if max(top_line_widths) <= img.width - padding * 2:
                    break
                top_font_size -= 1

            # Calculate the font size for the bottom text
            max_bottom_font_size = int(img.width / 10)
            bottom_font_size = max_bottom_font_size

            # Adjust the font size until the bottom text fits within the image width
            while True:
                bottom_line_widths = [text_draw.textsize(line, font=PIL.ImageFont.truetype(font_path, bottom_font_size))[0] for line in bottom_text_lines]
                if max(bottom_line_widths) <= img.width - padding * 2:
                    break
                bottom_font_size -= 1

            # Set the initial height for the top text
            top_text_height = 0

            # Draw each line of the top text on the image
            for line, font_size in zip(top_text_lines, [top_font_size, top_font_size]):
                font = PIL.ImageFont.truetype(font_path, font_size)
                text_width, text_height = text_draw.textsize(line, font=font)
                x = (img.width - text_width) // 2
                y = padding + top_text_height
                text_draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
                top_text_height += text_height

            # Set the initial height for the bottom text
            bottom_text_height = 0

            # Draw each line of the bottom text on the image
            for line, font_size in zip(bottom_text_lines, [bottom_font_size, bottom_font_size]):
                font = PIL.ImageFont.truetype(font_path, font_size)
                text_width, text_height = text_draw.textsize(line, font=font)
                x = (img.width - text_width) // 2
                y = img.height - padding - text_height - bottom_text_height
                text_draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
                bottom_text_height += text_height

            # Combine the original image with the text overlay
            composite_image = PIL.Image.alpha_composite(img, text_image)
            
            # save the resulting image
            output_path = f"{dannybot}\\cache\\ffmpeg\\output\\{frame}"
            composite_image.save(output_path)
    repack_gif()

    return

# dalle shit
# Communicate with the DALL-E API and ask it to generate images based on the prompt
async def generate_images(prompt: str) -> typing.List[io.BytesIO]:
    async with aiohttp.ClientSession() as session:
        async with session.post(DALLE_API, json={"prompt": prompt}) as response:
            if response.status == 200:
                logger.info("DALL-E server is OK")
                response_data = await response.json()
                
                # Convert the base64-encoded image strings to BytesIO objects
                images = [
                    io.BytesIO(base64.decodebytes(bytes(image, "utf-8")))
                    for image in response_data["images"]
                ]
                return images
            else:
                return None


# Generate the images for a DALL-E 3x3 grid collage
def make_collage_sync(images: typing.List[io.BytesIO], wrap: int) -> io.BytesIO:
    # Convert the images to numpy arrays
    image_arrays = [numpy.array(Image.open(image)) for image in images]
    
    image_count = 1
    for image in images:
        logger.info(f"{image_count} image(s) generated out of 9")
        image_count += 1
        image.seek(0)
    
    # Arrange the images into a 3x3 grid
    collage_rows = [
        numpy.hstack(image_arrays[i: i + wrap])
        for i in range(0, len(image_arrays), wrap)
    ]
    collage_array = numpy.vstack(collage_rows)
    
    # Create a PIL image from the collage array
    collage_image = Image.fromarray(collage_array)
    
    # Save the collage as a BytesIO object
    collage_bytes = io.BytesIO()
    collage_image.save(collage_bytes, format=DALLE_FORMAT)
    
    logger.info("Attempting to generate 3x3 collage")
    collage_bytes.seek(0)
    return collage_bytes

async def make_collage(images: typing.List[io.BytesIO], wrap: int) -> io.BytesIO:
    # Use asyncio's run_in_executor to run the synchronous collage generation in a separate thread or process
    collage_bytes = await asyncio.get_running_loop().run_in_executor(
        None, make_collage_sync, images, wrap
    )
    logger.info("3x3 collage generated")
    return collage_bytes

# generate list from directory of files
def listgen(directory):
    list =  os.listdir(directory)
    string = ', '.join(list)
    return string
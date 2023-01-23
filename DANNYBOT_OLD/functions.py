import json
import os
import random
import re
import sys
import urllib
import urllib.request
import PIL

import requests
from dotenv import load_dotenv
from PIL import (GifImagePlugin, Image, ImageColor, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps, ImageSequence)

load_dotenv()

# epic swag gif tools


def unpack_gif(file):
    os.system(
        f'ffmpeg -i "{file}" -vf fps=25 -vsync 0 "I:\\Dannybot\\cogs\\cache\\GIF\\temp%04d.png" -y')
    return


def repack_gif():
    os.system(f'ffmpeg -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\temp%04d.png.png" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" I:\\Dannybot\\cogs\\cache\\GIF\\output\\palette.png -y')
    os.system(f'ffmpeg -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\temp%04d.png.png" -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\palette.png" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 8M "I:\\Dannybot\\cogs\\cache\\outgif.gif" -y')
    return


def repack_gif_shittify():
    os.system(f'ffmpeg -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\temp%04d.png.jpg" -lavfi "scale=256x256,fps=25,palettegen=max_colors=256:stats_mode=diff" I:\\Dannybot\\cogs\\cache\\GIF\\output\\palette.png -y')
    os.system(f'ffmpeg -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\temp%04d.png.jpg" -i "I:\\Dannybot\\cogs\\cache\\GIF\\output\\palette.png" -lavfi "fps=25,mpdecimate,paletteuse=dither=none" -fs 8M "I:\\Dannybot\\cogs\\cache\\outgif.gif" -y')
    return


def cleanup_ffmpeg():
    for file in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
        if '.png' in file:
            os.remove('I:\\Dannybot\\cogs\\cache\\GIF\\'+file)
    for file in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF\\output'):
        if '.png' in file:
            os.remove('I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+file)

def infoload(attribute):
    # opens a json file containing any key attributes of Dannybot, such as it's prefix
    with open("info.json", "r") as jsonfile:
        data = jsonfile.read()  # open the json
        info = json.loads(data)  # read the json
        # send whichever attribute is passed with this function
        return str(info[attribute])


def fileCount(folder):
    total = 0  # set total to 0 to begin with
    # recursively walk down the folder passed into the function
    for root, dirs, files in os.walk(folder):

        total += len(files)  # add each file found to total
    return total  # send the total


def get_size(bytes, suffix="B"):
    factor = 1024  # The amount of __bytes per level
    for unit in [
        "",
        "K",
        "M",
        "G",
        "T",
        "P",
    ]:  # I have it go up to petabytes for no reason
        if bytes < factor:
            # calculate which suffix it needs by number of bytes
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def badregexcode(datalist, dataentry):
    with open(
        "I:\\Dannybot\\cogs\\InternalFiles\\RegexShit\\" + datalist + "_char"
    ) as f:
        entry = f.readlines()
        entry = [x.rstrip() for x in entry]
    with open(
        "I:\\Dannybot\\cogs\\InternalFiles\\RegexShit\\" + datalist + "_checker"
    ) as f:
        entryalias = f.readlines()
        entryalias = [x.rstrip() for x in entryalias]
    aru = " ".join(dataentry[:])
    inp = re.sub("[^a-z]", "", aru.lower())
    sort = [0] * len(entry)
    for i in range(0, len(entry)):
        sort[i] = i
    random.shuffle(sort)
    for i2 in range(
        0, len(entry)
    ):
        inputStripped = inp.strip() 
        aliasStripped = re.sub(
            "[^a-z]", "", entryalias[sort[i2]].lower().strip())
        entrystripped = re.sub("[^a-z]", "", entry[sort[i2]].lower().strip())
        if (inputStripped in entrystripped) or inputStripped in aliasStripped:
            break
    sort[i2]
    results = entry[sort[i2]]
    return results


def undertext(name):
    # character overrides
    if name == "danny":
        name = "https://cdn.discordapp.com/attachments/560608550850789377/1005989141768585276/dannyportrait1.png"
    elif name == "danny-funny":
        name = "https://cdn.discordapp.com/attachments/560608550850789377/1005999509496660060/dannyportrait3.png"
    elif name == "danny-angry":
        name = "https://cdn.discordapp.com/attachments/560608550850789377/1005989142825553971/dannyportrait4.png"
    elif name == "danny-pissed":
        name = "https://cdn.discordapp.com/attachments/560608550850789377/1005989142083145828/dannyportrait2.png"
    elif name in ["flashlight", "ezo", "ezogaming"]:
        name = "https://cdn.discordapp.com/attachments/1063552619110477844/1063552733170384926/FFlash.png"
    elif name == "incine":
        name = "https://cdn.discordapp.com/attachments/1063552619110477844/1063552737435992084/FIncine.png"
    elif name == "pizzi":
        name = "https://cdn.discordapp.com/attachments/1063552619110477844/1063552743626780732/FPizzi.png"
    elif name == "cris":
        name = "https://cdn.discordapp.com/attachments/1063552619110477844/1063552816397951037/FCris.png"
    elif name == "seki":
        name = "https://cdn.discordapp.com/attachments/1063552619110477844/1063738177212399658/sekiportrait1.png"
    else:
        name = name

    # link overrides
    if name.startswith("https://"):
        name = "custom&url=" + name
    return name


def gettenor(url=''):
    apikey = "8FMRE051ZV31"
    gifid = url[url.rindex('-')+1:]
    r = requests.get(
        "https://api.tenor.com/v1/gifs?ids=%s&key=%s&media_filter=minimal" % (gifid, apikey))

    if r.status_code == 200:
        gifs = json.loads(r.content)
    else:
        gifs = None
    return gifs['results'][0]['media'][0]['gif']['url']


async def message_history_img_handler(ctx):
    channel = ctx.message.channel
    extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'gif','PNG', 'JPG', 'JPEG', 'GIF', 'BMP', 'WEBP', 'GIF']
    async for msg in channel.history(limit=500):
        if len(msg.attachments) > 0:
            ext = msg.attachments[0].url.split('.')[-1]
            if ext in extensions:
                return msg.attachments[0].url
        if 'http' in msg.content:
            if 'https://tenor.com/view/' in msg.content:
                a = (str(gettenor(msg.content)))
                return a
            else:
                aa = str(msg.content)
                ext = aa.split('.')[-1]
                if ext in extensions:
                    a = re.findall("(?=http).*?(?= |\n|$)", msg.content)[0]
                    a = a.split('?')[0]
                    return a


async def message_history_audio_handler(ctx):
    channel = ctx.message.channel
    extensions = ['wav', 'ogg', 'mp3', 'flac', 'aiff', 'opus', 'm4a', 'oga', 'WAV', 'OGG', 'MP3', 'FLAC', 'AIFF', 'OPUS', 'M4A', 'OGA']
    async for msg in channel.history(limit=500):
        if len(msg.attachments) > 0:
            ext = msg.attachments[0].url.split('.')[-1]
            if ext in extensions:
                return msg.attachments[0].url
        if 'http' in msg.content:
            aa = str(msg.content)
            ext = aa.split('.')[-1]
            if ext in extensions:
                a = re.findall("(?=http).*?(?= |\n|$)", msg.content)[0]
                a = a.split('?')[0]
                return a


async def message_history_video_handler(ctx):
    channel = ctx.message.channel
    extensions = ['mp4', 'avi', 'mpeg', 'mpg', 'webm', 'mov', 'mkv', 'MP4', 'AVI', 'MPEG', 'MPG', 'WEBM', 'MOV', 'MKV']
    async for msg in channel.history(limit=500):
        if len(msg.attachments) > 0:
            ext = msg.attachments[0].url.split('.')[-1]
            if ext in extensions:
                return msg.attachments[0].url
        if 'http' in msg.content:
            aa = str(msg.content)
            ext = aa.split('.')[-1]
            if ext in extensions:
                a = re.findall("(?=http).*?(?= |\n|$)", msg.content)[0]
                a = a.split('?')[0]
                return a


# returns a list of [url,text] for url and text
async def resolve_args(ctx, args, attachments):
    try:
        if 'http' in args[0]:
            url = args[0]
            kys = args[1:]
            text = ' '.join(kys)
            return [url.split('?')[0], text]
        elif attachments:
            url = attachments[0].url
            text = ' '.join(args)
            return [url.split('?')[0], text]
        else:
            url = await message_history_img_handler(ctx)
            text = ' '.join(args)
            return [url, text]
    except IndexError:
        if attachments:
            url = attachments[0].url
            text = ' '.join(args)
            return [url.split('?')[0], text]
        else:
            url = await message_history_img_handler(ctx)
            text = ' '.join(args)
            return [url, text]

# meme shit


def make_meme(Top_Text, Bottom_Text, path, is_gif):
    if (is_gif):
        for frame in os.listdir('I:\\Dannybot\\cogs\\cache\\GIF'):
            if '.png' in frame:
                img = PIL.Image.open('I:\\Dannybot\\cogs\\cache\\GIF\\'+frame)
                imageSize = img.size
                fontSize = int(imageSize[1]/5)
                font = ImageFont.truetype("impactjpn.otf", fontSize)
                topTextSize = font.getsize(Top_Text)
                bottomTextSize = font.getsize(Bottom_Text)
                while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
                    fontSize = fontSize - 1
                    font = ImageFont.truetype("impactjpn.otf", fontSize)
                    topTextSize = font.getsize(Top_Text)
                    bottomTextSize = font.getsize(Bottom_Text)
                topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
                topTextPositionY = 0
                topTextPosition = (topTextPositionX, topTextPositionY)
                bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
                bottomTextPositionY = imageSize[1] - bottomTextSize[1]
                bottomTextPosition = (
                    bottomTextPositionX, bottomTextPositionY - 10)
                OutlineBaseWidth = font.getsize("Base Outline Width")
                draw = ImageDraw.Draw(img)
                draw.text(topTextPosition, Top_Text, (255, 255, 255), font=font, stroke_width=(
                    OutlineBaseWidth[0]//200), stroke_fill=(0, 0, 0))
                draw.text(bottomTextPosition, Bottom_Text, (255, 255, 255), font=font, stroke_width=(
                    OutlineBaseWidth[0]//200), stroke_fill=(0, 0, 0))
                img.save('I:\\Dannybot\\cogs\\cache\\GIF\\output\\'+frame+".png")
                print("frame " + frame + " processed")
    else:
        img = PIL.Image.open(path)
        imageSize = img.size
        fontSize = int(imageSize[1]/5)
        font = ImageFont.truetype("impactjpn.otf", fontSize)
        topTextSize = font.getsize(Top_Text)
        bottomTextSize = font.getsize(Bottom_Text)
        while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
            fontSize = fontSize - 1
            font = ImageFont.truetype("impactjpn.otf", fontSize)
            topTextSize = font.getsize(Top_Text)
            bottomTextSize = font.getsize(Bottom_Text)
        topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
        topTextPositionY = 0
        topTextPosition = (topTextPositionX, topTextPositionY)
        bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
        bottomTextPositionY = imageSize[1] - bottomTextSize[1]
        bottomTextPosition = (bottomTextPositionX, bottomTextPositionY - 10)
        OutlineBaseWidth = font.getsize("Base Outline Width")
        draw = ImageDraw.Draw(img)
        draw.text(topTextPosition, Top_Text, (255, 255, 255), font=font,
                  stroke_width=(OutlineBaseWidth[0]//200), stroke_fill=(0, 0, 0))
        draw.text(bottomTextPosition, Bottom_Text, (255, 255, 255), font=font,
                  stroke_width=(OutlineBaseWidth[0]//200), stroke_fill=(0, 0, 0))
        img.save('I:\\Dannybot\\cogs\\cache\memeout.png')
    if (is_gif):
        repack_gif()
        return
    else:
        return

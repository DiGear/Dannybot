import os
import sys
import typing
from time import sleep

import discord
import requests
from discord import File
from discord.ext import commands
from discord.file import File

from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')

inprocess = True
global processing
processing = False  # both the inprocess and processing globals are used for the purpose of ratelimiting commands that are intensive


class Audio(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: audio")

    @commands.command(
        description="Renders a midi file with a random soundfont, and sends the resulting mp3. You can also choose a specific soundfont from a list of available ones.",
        brief="Applies a selectable soundfont to a midi file"
    )
    async def midislap(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment", *, SF2: typing.Optional[str] = "Random"):
        soundfontchoice = "NULL"
        await ctx.send('Processing... While we wait, did you know what soundfonts are available? The list is... uh...\n8bit\nbw2\ndppt\nfrlg\ngba\ngeneral\nmc\nn64\nsega\nsgm\nsm64\ntouhou', delete_after=20)
        with open(f'midislap.mid', 'wb') as f:
            try:  # this assume the image was linked to, and attempts to download the file via the link
                f.write(requests.get(File_Url).content)
                f.close
            except:  # if false
                SF2 = File_Url  # interpret the file_url variable as a value to be used in the command instead
                # set the url as an attachment link
                File_Url = ctx.message.attachments[0].url
                # download the contents of the url
                f.write(requests.get(File_Url).content)
                f.close
            sf2s = ["sm64.bat", "bw2.bat", "frlg.bat", "8bit.bat", "sega.bat", "touhou.bat",
                    "mc.bat", "gba.bat", "n64.bat", "dppt.bat", "general.bat", "sgm.bat"]
            if (SF2 == "Random"):  # error handler 1, sets the effect value to its default if one was provided, or if the bot cant find it
                SF2 = random.choice(sf2s)
            # error handler 2, sets the effect value to its default if one was provided, or if the bot cant find i
            if (SF2 == "File_Is_Attachment"):
                SF2 = random.choice(sf2s)
            else:
                # choose a random type from the array
                soundfontchoice = (SF2 + ".bat")
            if (os.path.exists(soundfontchoice)):
                os.system(soundfontchoice)
                # ffmpeg normalizes the mp3 volume
                os.system(
                    'ffmpeg -y -i slapped.wav -vn -ar 44100  -ac 2 -b:a 96k slappednorm.mp3')
                with open(f'slappednorm.mp3', 'rb') as f:  # prepare the file for sending
                    await ctx.reply('Midislapped with ' + str(soundfontchoice).replace('.bat', '.sf2'), file=File(f, 'midislap.mp3'))
                    f.close
            else:
                SF2 = random.choice(sf2s)
                soundfontchoice = random.choice(sf2s)
                os.system(soundfontchoice)
                # ffmpeg normalizes the mp3 volume
                os.system(
                    'ffmpeg -y -i slapped.wav -vn -ar 44100  -ac 2 -b:a 96k slappednorm.mp3')
                with open(f'slappednorm.mp3', 'rb') as f:  # prepare the file for sending
                    await ctx.reply('Midislapped with ' + str(soundfontchoice).replace('.bat', '.sf2'), file=File(f, 'midislap.mp3'))
                    f.close

    @commands.command(
        description="Use UVR to separate the vocals and instrumental from a provided file, and sends the results as mp3 files.",
        brief="Splits audio into vocals and instrumental using AI"
    )
    async def acapella(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        global processing  # defining a global to be used for ratelimiting :)
        # this checks to see if the image is an attachment or a link
        if(File_Url == "File_Is_Attachment"):
            # Image is an attachment
            Link_To_File = ctx.message.attachments[0].url
        else:
            Link_To_File = File_Url  # Image is a link

        if(processing != True):  # checks if an instance of d.split is already running, and cancels processing if so
            processing = True  # marks a d.split command as in progress
            # this code block writes the AV data to a file
            with open(f'I:\\Dannybot\\cogs\\dependencies\\UVR\\audio.mp3', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            await ctx.send("Splitting. Please wait...")
            # open dependencies\\UVR
            os.system('cd I:\\Dannybot\\cogs\\dependencies\\UVR')
            # set cmds working directory to the dependencies\\UVR directory
            os.chdir('I:\\Dannybot\\cogs\\dependencies\\UVR')
            # run UVR on gpu
            os.system('python inference.py --input audio.mp3 --gpu 0')
            # ffmpeg to convert wav to mp3
            os.system(
                "ffmpeg -i audio_Instruments.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Instruments.mp3 -y")
            # ffmpeg to convert wav to mp3
            os.system(
                "ffmpeg -i audio_Vocals.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Vocals.mp3 -y")
            with open(f'audio_Instruments.mp3', 'rb') as f:
                try:  # this code block attempts to send the instrumental and cancels if the file is too large
                    await ctx.reply(file=File(f, 'Inst.mp3'))
                except:
                    await ctx.reply("The file(s) requested is too large to send through discord. Please ask the bot owner to send it to you", mention_author=True)
                    f.close
            with open(f'audio_Vocals.mp3', 'rb') as f:
                try:  # this code block attempts to send the vocals and cancels if the file is too large
                    await ctx.reply(file=File(f, 'Vocal.mp3'))
                except:
                    await ctx.reply("The file(s) requested is too large to send through discord. Please ask the bot owner to send it to you", mention_author=True)
                    f.close
                    os.chdir('I:\\Dannybot')
            # marks the d.split command as finished, allowing for another d.split to be ran
            processing = False
        else:
            await ctx.reply("A split is currently in progress, please wait for the current split to finish.")

    @commands.command(
        description="Use UVR + demucs to separate song stems from a provided file, and sends the results as mp3 files.",
        brief="Splits audio into stems using AI"
    )
    async def stems(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        global processing  # defining a global to be used for ratelimiting :)
        if(File_Url == "File_Is_Attachment"):
            # Image is an attachment
            Link_To_File = ctx.message.attachments[0].url
        else:
            Link_To_File = File_Url  # Image is a link

        if(processing != True):  # checks if an instance of d.split is already running, and cancels processing if so
            processing = True  # marks a d.split command as in progress
            with open(f'I:\\Dannybot\\cogs\\dependencies\\Demucs\\audio.mp3', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            await ctx.send("Splitting. Please wait...")
            os.system('cd I:\\Dannybot\\cogs\\dependencies\\Demucs')
            os.chdir('I:\\Dannybot\\cogs\\dependencies\\Demucs')
            os.system(
                'demucs "I:\\Dannybot\\cogs\\dependencies\\Demucs\\audio.mp3" --segment 8 --mp3 --mp3-bitrate 128')
            os.chdir('I:\\Dannybot')
            await ctx.reply(file=File('I:\Dannybot\\cogs\\dependencies\\Demucs\\separated\\mdx_extra_q\\audio\\vocals.mp3'))
            await ctx.reply(file=File('I:\Dannybot\\cogs\\dependencies\\Demucs\\separated\\mdx_extra_q\\audio\\bass.mp3'))
            await ctx.reply(file=File('I:\Dannybot\\cogs\\dependencies\\Demucs\\separated\\mdx_extra_q\\audio\\drums.mp3'))
            await ctx.reply(file=File('I:\Dannybot\\cogs\\dependencies\\Demucs\\separated\\mdx_extra_q\\audio\\other.mp3'))
            processing = False
        else:
            await ctx.reply("A split is currently in progress, please wait for the current split to finish.")

async def setup(client):
    await client.add_cog(Audio(client))

import asyncio
import os
import subprocess
import sys
import traceback
from random import randrange

import discord
import furl
from cleverwrap import CleverWrap
from discord import Member
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

print("DANNYBOT IS STARTING UP... PLEASE WAIT...")  # prints separator

load_dotenv()

inprocess = True
global processing
processing = False  # both the inprocess and processing globals are used for the purpose of ratelimiting commands that are intensive

devs = [
    343224184110841856,  # Danny
    158418656861093888,  # EzoGaming
    249411048518451200,  # Rotty
    847276836172988426  # Dannybot
]

lastusedcommand = "none"  # defining this for the message handler code
lastsentimage = "none"

# load configs from .env
token = os.getenv("TOKEN")
cw = CleverWrap(os.getenv("CLEVERBOT_KEY"))

debug_mode = False
intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("d.", "D.", "ratio + ", "#"),
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=3),
    intents=intents,
)

@client.event
async def on_ready():
    print("all modules imported")  
    print("primary script loaded")
    print("loading all imported modules")


@client.event
async def on_message(input):
    # Make sure we aren't logging anything in the logs channel
    if "971178342550216705" not in str(input.channel.id):
        # Check for command usage
        if (
            input.content.startswith("d.")
            or input.content.startswith("D.")
            or input.content.startswith("ratio + ")
            or input.content.startswith("<@847276836172988426>")
            or input.content.startswith("#")
        ):
            print(
                str(input.author.name)
                + " "
                + str(input.author.id)
                + " issued "
                + input.content
            )
            await client.get_channel(971178342550216705).send(str(input.author.name) + " " + str(input.author.id) + " issued " + input.content)


    # Cleverbot Hook
    if "talk-to-dannybot" in str(input.channel.name) and not input.author.bot:
            if "new conversation" in input.content:
                cw.reset()
            elif "> " in input.content:
                print("skipped")
            else:
                parsed_data = input.content.replace("dannybot", "")
                parsed_data = parsed_data + str(" ")
                print(input.author.name + ": " + parsed_data)
                await client.get_channel(971178342550216705).send(
                    "**CLEVERBOT LOGS** "
                    + input.author.name
                    + " "
                    + str(input.author.id)
                    + ": "
                    + parsed_data
                )
                await input.channel.send(cw.say(parsed_data), reference=input)
    else:
        if (debug_mode):
            if (
                input.content.startswith("d.")
                or input.content.startswith("D.")
                or input.content.startswith("ratio + ")
                or input.content.startswith("<@847276836172988426>")
                or input.content.startswith("#")
            ):
                if (input.author.id not in devs):
                    await input.channel.send("Developer mode is active. Only verified developers can interact with the bot at this time.")
                else:
                    await client.process_commands(input)
        else:
            await client.process_commands(input)

# error handler
@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, "on_error"):
        return

    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound,)

    error = getattr(error, "original", error)

    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f"{ctx.command} has been disabled.")

    elif isinstance(error, commands.errors.NotOwner):
        await ctx.send(f"{ctx.command} requires a higher permission level.")

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
        except discord.HTTPException:
            pass
    else:
        await ctx.send(
            "An undefined error has occured.\n```\n"
            + str(error.__traceback__)
            + "\n"
            + str(error)
            + "```\nIf you are seeing this, ping either FDG or EzoGaming."
        )
        print("Ignoring exception in command {}:".format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )


@client.command(
    description="Delete the most recent command output in the current channel. This only affects Dannybot.",
    brief="Undo the last command output"
)
async def undo(ctx):
    channel = ctx.message.channel
    async for msg in channel.history(limit=500):
        if msg.author.id == 847276836172988426:
            await msg.delete()
            return


@client.command(
    description="This is an owner only command. It allows for any module to be reloaded on the fly.",
    brief="Debug tool for modules"
)
@commands.is_owner()
async def reload(ctx, module):
    await client.unload_extension(f"cogs.{module}")
    await client.load_extension(f"cogs.{module}")
    await ctx.send(f"Reloaded {module} module!")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print("imported module: " + f"{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())
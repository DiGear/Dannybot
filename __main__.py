# this is the file that boots up every other file.
# you should never need to touch anything in here, other than to change the list of developers.
# the developer list is located at line 25
import asyncio
import os
import sys
import time
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from functions import *

load_dotenv()

bot = commands.Bot(
    command_prefix=("d2."),
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=3),
    intents=discord.Intents.all(),
)

# debug mode is a setting which makes the bot only respond to commands from the user IDs listed in "devs"
debug_mode = True
# put your user ID here, as well as any other user IDs that you would like to be able to bypass debug mode
devs = [
    343224184110841856,  # Danny
    158418656861093888,  # EzoGaming
]

# print a success message upon boot, and then change the bots activity
@bot.event
async def on_ready():
    print(f"{bot.user} successfully booted up on discord.py version {discord.__version__}")
    await bot.change_presence(activity=discord.Activity(type=discord.Activity(name="for d.help", type=3)))
    return

# this utilizes the above debug mode features to check for verified developers, and process command input
@bot.event
async def on_message(input):
    if (debug_mode and input.content.startswith(bot.command_prefix) and input.author.id not in devs):
        await input.channel.send("Developer mode is active. Only verified developers can interact with the bot at this time.")
    else:
        await bot.process_commands(input)

# error handling code
@bot.event
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

# this is a ping command and it's pretty self-explanatory
@bot.command(
    description="Calculate bot latency using time.monotonic(), and send the results.",
    brief="Sends the current bot latency"
    )
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Ping is...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Ping is {int(ping)}ms")
    print(f'Dannybot was pinged at {int(ping)}ms')

# say command because every good bot should be a vessel for its creator to speak through
@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, args):
    # this literally just repeats what is stored in "args"
    await ctx.send(args)
    # delete the command message, leaving only what Dannybot sends
    await ctx.message.delete()

# this command reloads a specified cog. used for testing, you can call this command to update code on a cog without restarting the whole bot
@bot.command(
    description="This is an owner only command. It allows for any module to be reloaded on the fly.",
    brief="Debug tool for modules"
)
@commands.is_owner()
async def reload(ctx, module):
    await bot.unload_extension(f"cogs.{module}")
    await bot.load_extension(f"cogs.{module}")
    await ctx.send(f"Reloaded {module} module!")

# stage all of our cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print("imported module: " + f"{filename[:-3]}")

# load all of our cogs and start the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
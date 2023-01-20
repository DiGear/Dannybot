import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#command_prefix=commands.when_mentioned_or("d.", "D.", "ratio + ", "#"),

bot = commands.Bot(
    command_prefix=("d2."),
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=3),
    intents=discord.Intents.all(),
)

#debug mode shit
debug_mode = True
devs = [
    343224184110841856,  # Danny
    158418656861093888,  # EzoGaming
]

@bot.event
async def on_ready():
    print(f"{bot.user} successfully booted up on discord.py version {discord.__version__}")
    await bot.change_presence(activity=discord.Activity(type=discord.Activity(name="for d.help", type=3)))
    return

@bot.event
async def on_message(input):
    if (debug_mode and input.content.startswith(bot.command_prefix) and input.author.id not in devs): #debug mode shit
        await input.channel.send("Developer mode is active. Only verified developers can interact with the bot at this time.")
    else:
        await bot.process_commands(input)

@bot.command()
async def hi(ctx):
    await ctx.send("hi")

@bot.command(
    description="This is an owner only command. It allows for any module to be reloaded on the fly.",
    brief="Debug tool for modules"
)
@commands.is_owner()
async def reload(ctx, module):
    await bot.unload_extension(f"cogs.{module}")
    await bot.load_extension(f"cogs.{module}")
    await ctx.send(f"Reloaded {module} module!")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print("imported module: " + f"{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
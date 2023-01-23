import time

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
from PyDictionary import PyDictionary

from functions import *

# add dannybot modules to path
sys.path.insert(1, '/modules')

dictionary = PyDictionary()


class Essentials(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded module: essentials")

    @commands.command(
        description="Calculate bot latency using time.monotonic(), and send the results.",
        brief="Sends the current bot latency"
        )
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Ping is...")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Ping is {int(ping)}ms")
        print(f'Ping {int(ping)}ms')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def say(self, ctx, *, args):
        # this literally just repeats what is stored in "args"
        await ctx.send(args)
        # delete the command message, leaving only what Dannybot sends
        await ctx.message.delete()

async def setup(client):
    await client.add_cog(Essentials(client))

# log command usage to the console and to a specified channel
import os

import discord
from discord.ext import commands

# set this to your logging channel ID
logs_channel = 971178342550216705


class logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        # make sure that we're only logging commands, rather than every message
        if input.content.startswith(self.bot.command_prefix):
            #send all relevant information relating to command usage to our logs channel
            await self.bot.get_channel(logs_channel).send(f"{input.author.name} {input.author.id} issued {input.content}")
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))

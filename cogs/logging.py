# log command usage to the console and to a specified channel
import os

import discord
from discord.ext import commands

class cleverbot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(cleverbot(bot))

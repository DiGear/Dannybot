# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        for react in ['python', 'py']:
            if react in message.content.lower():
                await message.add_reaction('🐍')
        for react in ['java', 'jar']:
            if react in message.content.lower() and not "javascript" in message.content.lower():
                await message.add_reaction('♨️')
        for react in ['javascript', 'js']:
            if react in message.content.lower():
                await message.add_reaction('🐒')
        for react in ['ruby', 'rb']:
            if react in message.content.lower():
                await message.add_reaction('💎')
        for react in ['true', 'truth', "fact"]:
            if react in message.content.lower():
                await message.add_reaction('👏')
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))
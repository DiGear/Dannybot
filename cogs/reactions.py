# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        reactions = {
            '🐍': ['python', 'py'],
            '♨️': ['java', 'jar'],
            '💎': ['ruby', 'rb'],
            '👏': ['true', 'truth', 'fact']
        }
        for emoji, keywords in reactions.items():
            for keyword in keywords:
                if keyword in message.content.lower():
                    await message.add_reaction(emoji)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))
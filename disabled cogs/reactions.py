# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.lower().startswith("balls in"):
            await message.channel.send("https://cdn.discordapp.com/attachments/947963019319709777/1080006889468862555/maxresdefault.png", reference=message)
        elif message.content.lower().startswith("balls out"):
            await message.channel.send("https://cdn.discordapp.com/attachments/947963019319709777/1080011687979122779/latest.png", reference=message)
        reactions = {
            '🐍': ['python', 'py'],
            '♨️': ['java', 'jar'],
            '💎': ['ruby', 'rb'],
            '👏': ['true', 'truth', 'fact'],
            '✋': ['yay'],
            '💥': ['yay']
        }
        for emoji, keywords in reactions.items():
            for keyword in keywords:
                if keyword in message.content.lower():
                    await message.add_reaction(emoji)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))
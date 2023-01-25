# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        if talking_channel not in str(input.channel.name) and not input.author.bot:
            
            # dannybot
            if "dannybot" in str(input.content).lower():
                await input.channel.send("me", reference=input)
            
            # slur    
            if slur in str(input.content).lower():
                await input.channel.send("SLUR DETECTED")
                await input.channel.send(f'FUCK YOU {input.author.name}')
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))

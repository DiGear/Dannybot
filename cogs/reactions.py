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
            if any(slurs in str(input.content).lower() for slurs in slur):
                if any(slurs not in input.author.name.lower() for slurs in slur):
                    slur_sayer = str(input.author.display_name).upper()
                    await input.channel.send(f"SLUR DETECTED\nFUCK YOU {slur_sayer}")
                else:
                    await input.channel.send('SLUR DETECTED\nFUCK YOU')
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))

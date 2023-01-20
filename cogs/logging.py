# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *


class logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        # make sure that we're only logging commands, rather than every message
        if input.content.startswith(self.bot.command_prefix):
            # send all relevant information relating to command usage to our logs channel
            await self.bot.get_channel(logs_channel).send(f"{input.author.name} {input.author.id} issued {input.content}")
            return
        # log all cleverbot activity in a different manner
        if "talk-to-dannybot" in str(input.channel.name) and not input.author.bot:
            # send all relevant information pertaining to the current cleverbot api usage
            await self.bot.get_channel(logs_channel).send(f"**CLEVERBOT LOGS** | *{input.author.name} {input.author.id} said:* {input.content}")
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))

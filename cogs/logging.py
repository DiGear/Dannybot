# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)


class logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Check if the message starts with any of the bot's prefixes
        for prefix in dannybot_prefixes:
            if message.content.startswith(prefix):
                # Send command usage information to the logs channel
                log_message = f"{message.author.name} ({message.author.id}) issued: {message.content}"
                await self.bot.get_channel(logs_channel).send(log_message)
            break

async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))
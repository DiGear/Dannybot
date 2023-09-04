# log command usage to the console and to a specified channel

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)


class logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        log_channel = self.bot.get_channel(logs_channel)
        if any(message.content.startswith(prefix) for prefix in dannybot_prefixes):
            log_message = f"{message.author.global_name} ({message.author.id}) issued: {message.content}"
            await log_channel.send(log_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))
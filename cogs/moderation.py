# obligatory moderation commands - FDG

# this shit is still empty lol

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)


class moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot):
    await bot.add_cog(moderation(bot))

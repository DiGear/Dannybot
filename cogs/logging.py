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
            log_message = f"{message.author.name} ({message.author.id}) issued: {message.content}"
            await log_channel.send(log_message)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        log_channel = self.bot.get_channel(logs_channel)
        command_name = interaction.data["name"]
        user = interaction.user
        options = interaction.data.get("options", [])
        args = {option["name"]: option["value"] for option in options}
        args_str = " ".join(f"{k} = {repr(v)}" for k, v in args.items())
        if interaction.type == InteractionType.application_command:
            log_message = (
                f"{user.name} ({user.id}) issued: /{command_name} {args_str}"
            )
            await log_channel.send(log_message)


async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))

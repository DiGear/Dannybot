# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        content = message.content.lower()
        if content.startswith("balls in"):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/896060285763325962/1285826127272611840/DOEvKrgUMAEn_tO.png",
                reference=message,
            )
        elif content.startswith("balls out"):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/947963019319709777/1080011687979122779/latest.png",
                reference=message,
            )
        elif "cigarette" in content and not message.author.bot:
            await message.channel.send(
                "https://tenor.com/view/500-cigarettes-the-orville-gif-7999465420984481267",
                reference=message,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))

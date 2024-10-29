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
                "https://cdn.discordapp.com/attachments/886788323648094219/1298440117417017434/92kyi4ewfkha1.jpg",
                reference=message,
            )
        elif "cigarette" in content and not message.author.bot:
            await message.channel.send(
                "https://tenor.com/view/500-cigarettes-the-orville-gif-7999465420984481267",
                reference=message,
            )
        elif content.startswith("ourgh") and not message.author.bot:
            await message.channel.send(
                "Banned."
            )
        elif content.startswith("mommy"):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/900431883559661649/1259755505824436254/meme.gif",
                reference=message,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))

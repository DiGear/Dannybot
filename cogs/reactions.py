# if you can't find a variable used in this file its probably imported from here
from config import *


class reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reactions = {
            "🐍": ["python", "py"],
            "♨️": ["java", "jar"],
            "💎": ["ruby", "rb"],
            "👏": ["true", "truth", "fact"],
            "✋": ["yay"],
            "💥": ["yay"],
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        content = message.content.lower()
        if content.startswith("balls in"):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/947963019319709777/1080006889468862555/maxresdefault.png",
                reference=message,
            )
        elif content.startswith("balls out"):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/947963019319709777/1080011687979122779/latest.png",
                reference=message,
            )

        for emoji, keywords in self.reactions.items():
            if any(keyword in content for keyword in keywords):
                await message.add_reaction(emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(reactions(bot))

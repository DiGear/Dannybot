# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *


class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Display file counts for key directories in Dannybot", brief="Display file counts for key directories in Dannybot")
    async def db(self, ctx):
        # some of the directories here are hardcoded due to them being on other parts of my pc, unfortunately
        embed = discord.Embed(title="Dannybot File Totals", color=0xf77e9a)
        embed.add_field(name="Pizzi AI Image Files:", value=fileCount(f"{dannybot}\\database\\Dooter"), inline=True)
        embed.add_field(name="Pooter Files:", value=fileCount(f"{dannybot}\\database\\Pooter"), inline=True)
        embed.add_field(name="Leffrey Files:", value=fileCount(f"{dannybot}\\database\\Leffrey"), inline=True)
        embed.add_field(name="Femboy Files:", value=fileCount(f"{dannybot}\\database\\Femboy"), inline=True)
        embed.add_field(name="Fanboy Files:", value=fileCount(f"{dannybot}\\database\\Fanboy"), inline=True)
        embed.add_field(name="Video Files:", value=fileCount("C:\\Users\\weebm\\Videos"), inline=True)
        embed.add_field(name="Image Files:", value=fileCount("C:\\Users\\weebm\\Pictures"), inline=True)
        embed.add_field(name="GIF Files:", value=fileCount("C:\\Users\\weebm\\Pictures\\GIFS"), inline=True)
        embed.add_field(name="Glass Cup Images:", value=fileCount(f"{dannybot}\\database\\Glasscup"), inline=True)
        embed.add_field(name="Koishi Images:", value=fileCount(f"{dannybot}\\database\\Koishi"), inline=True)
        embed.add_field(name="Burger Files:", value=fileCount(f"{dannybot}\\database\\Burger"), inline=True)
        embed.add_field(name="Nekopara Files:", value=fileCount("E:\\Anime\\Nekopara\\"), inline=True)
        embed.add_field(name="Animal Girl Images:", value=fileCount(f"{dannybot}\\database\\Mimi"), inline=True)
        embed.add_field(name="Kemono Friends Files:", value=fileCount("E:\\Anime\\Kemono Friends\\"), inline=True)

        await ctx.reply(embed=embed, mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))

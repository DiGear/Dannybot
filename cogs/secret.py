# huh

# if you can't find a variable used in this file its probably imported from here
from config import *


class secret(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def eez(self, ctx, args):
        if args == 'nutz' or args == 'nuts':
            await ctx.reply("goteem", mention_author=True)
        else:
            return

    @commands.command(hidden=True)
    async def bruh(self, ctx):
        await ctx.reply("https://www.youtube.com/watch?v=beQMZ9-Ovs4", mention_author=True)

       
    @commands.command(hidden=True)
    async def poopoo(self, ctx):
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))

async def setup(bot: commands.Bot):
    await bot.add_cog(secret(bot))
# this is most likely gonna be necessary for expanding upon pooter later

# if you can't find a variable used in this file its probably imported from here
from config import *


class pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(aliases=['poo'], description="Send or recieve a file from a user-built archive of files. You can upload 9 files at a time, or not attach any files to view the archive instead.", brief="Send/Recieve files from a public archive.")
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        downloads = 1
        reaction = '✅'
        f_name = randhex(128)
        if ctx.message.attachments:
            for i in ctx.message.attachments:
                Link_To_File = i.url
                await ctx.send(f'Downloading... {downloads} of {len(ctx.message.attachments)}', delete_after=1)
                downloads += 1
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f:
                    f.write(requests.get(Link_To_File).content)
                    f.close
                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {Link_To_File}')
            await ctx.message.add_reaction(reaction)
        elif File_Url == None:
            pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
            with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                await ctx.reply(file=File(f, pooter_file))
        else:
                Link_To_File = File_Url
                await ctx.send("Downloading... (1 of 1)", delete_after=1)
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f:
                    f.write(requests.get(Link_To_File).content)
                    f.close
                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {Link_To_File}')
                await ctx.message.add_reaction(reaction)
                
    @commands.command(brief="Send 2 files from a public archive.")
    async def poopoo(self, ctx):
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))

async def setup(bot: commands.Bot):
    await bot.add_cog(pooter(bot))

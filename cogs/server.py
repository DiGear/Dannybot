# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *


class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['poo'], description="Send or recieve a file from a user-built archive of files. You can upload 9 files at a time, or not attach any files to view the archive instead.", brief="Send/Recieve files from a public archive.")
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        downloads = 1
        f_name = randhex(128)
        if ctx.message.attachments:
            for i in ctx.message.attachments:
                Link_To_File = i.url
                await ctx.send(f'Downloading... {downloads} of {len(ctx.message.attachments)}', delete_after=10)
                downloads += 1
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f:
                    f.write(requests.get(Link_To_File).content)
                    f.close
                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {Link_To_File}')
        elif File_Url == None:
            pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
            with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                await ctx.reply(file=File(f, pooter_file))
        else:
                Link_To_File = File_Url
                await ctx.send("Downloading... (1 of 1)", delete_after=10)
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f:
                    f.write(requests.get(Link_To_File).content)
                    f.close

    @commands.command(aliases=['catgirl'], description="Send a picture of an catgirl using the nekos.life API.", brief="Send a picture of an catgirl")
    async def neko(self, ctx):
        with requests.Session() as s:
            api_output = s.get("https://nekos.life/api/v2/img/neko")
        output = api_output.text
        x = json.loads(output, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        url = x.url
        await ctx.reply(url, mention_author=True)

    @commands.command(description="Send a Kemono Friends character from my personal collection.", brief="Send a picture of a chosen character from Kemono Friends")
    async def friend(self, ctx, *frien):
        aru2 = ezogaming_regex("Kemofure", frien)
        dir = f'{KemonoFriendsPath}\\' + aru2
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close

    @commands.command(description="Send a Nekopara character from my personal collection.", brief="Send a picture of a chosen character from Nekopara")
    async def nekopara(self, ctx, *frien):
        aru2 = ezogaming_regex("Nekopara", frien)
        dir = f'{NekoparaPath}\\' + aru2
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close

    @commands.command(description="Display file counts for key directories in Dannybot", brief="Display file counts for key directories in Dannybot")
    async def db(self, ctx):
        embed = discord.Embed(title="Dannybot File Totals", color=0xf77e9a)
        embed.add_field(name="Pizzi AI Image Files:", value=fileCount(f"{dannybot}\\database\\Dooter"), inline=True)
        embed.add_field(name="Pooter Files:", value=fileCount(f"{dannybot}\\database\\Pooter"), inline=True)
        embed.add_field(name="Leffrey Files:", value=fileCount(f"{dannybot}\\database\\Leffrey"), inline=True)
        embed.add_field(name="Femboy Files:", value=fileCount(f"{dannybot}\\database\\Femboy"), inline=True)
        embed.add_field(name="Fanboy Files:", value=fileCount(f"{dannybot}\\database\\Fanboy"), inline=True)
        embed.add_field(name="Video Files:", value=fileCount(VideosPath), inline=True)
        embed.add_field(name="Image Files:", value=fileCount(PicturesPath), inline=True)
        embed.add_field(name="GIF Files:", value=fileCount(GifsPath), inline=True)
        embed.add_field(name="Glass Cup Images:", value=fileCount(f"{dannybot}\\database\\Glasscup"), inline=True)
        embed.add_field(name="Koishi Images:", value=fileCount(f"{dannybot}\\database\\Koishi"), inline=True)
        embed.add_field(name="Burger Files:", value=fileCount(f"{dannybot}\\database\\Burger"), inline=True)
        embed.add_field(name="Nekopara Files:", value=fileCount(NekoparaPath), inline=True)
        embed.add_field(name="Animal Girl Images:", value=fileCount(f"{dannybot}\\database\\Mimi"), inline=True)
        embed.add_field(name="Kemono Friends Files:", value=fileCount(KemonoFriendsPath), inline=True)

        await ctx.reply(embed=embed, mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))

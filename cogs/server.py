# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *


class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['catgirl'], description="Send a picture of an catgirl using the nekos.life API.", brief="Send a picture of an catgirl")
    async def neko(self, ctx):
        with requests.Session() as s:
            api_output = s.get("https://nekos.life/api/v2/img/neko")
        output = api_output.text
        x = json.loads(output, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        await ctx.reply(x.url, mention_author=True)
        
    @commands.command(description="Send a picture of an animal girl.", brief="Send a picture of an animal girl")
    async def mimi(self, ctx):
        file_name = random.choice(os.listdir(MimiPath))
        with open(f'{MimiPath}\\{file_name}', 'rb') as f:
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
            
    @commands.command(description="Send a video from my personal collection.", brief="Send a video from my camera roll")
    async def vid(self, ctx):
        dir = VideosPath
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            
    @commands.command(description="Send a picture from my personal collection.", brief="Send a picture from my camera roll")
    async def img(self, ctx):
        dir = PicturesPath
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
    @commands.command(description="Send a picture of Leffrey.", brief="Send a picture of Leffrey")          
    async def leffrey(self, ctx):
        dir = f"{dannybot}\\database\\Leffrey"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            
    @commands.command(description="Send a GIF file.", brief="Send a GIF file")
    async def gif(self, ctx):
        dir = GifsPath
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, file_name), mention_author=True)
            f.close
            
    @commands.command(description="Send a picture of a femboy (anime).", brief="Send a picture of an anime femboy")
    async def femboy(self, ctx):
        dir = f"{dannybot}\\database\\Femboy"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'fem.png'), mention_author=True)
            
    @commands.command(description="Send a Fanboy and Chum Chum picture.", brief="Send a Fanboy and Chum Chum picture")
    async def fanboy(self, ctx):
        dir = f"{dannybot}\\database\\Fanboy"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'fan.png'), mention_author=True)
            
    @commands.command(description="Send a picture of a glass cup.", brief="Send a picture of a glass cup")
    async def glasscup(self, ctx):
        dir = f"{dannybot}\\database\\Glasscup"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'glass.png'), mention_author=True)
        
    @commands.command(description="Send a picture of a plastic cup.", brief="Send a picture of a plastic cup")
    async def plasticcup(self, ctx):
        dir = f"{dannybot}\\database\\Plasticcup"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'plastic.png'), mention_author=True)
            
    @commands.command(description="Send a picture of a burger.", brief="Send a picture of a burger")
    async def burger(self, ctx):
        dir = f"{dannybot}\\database\\Burger"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'burger.png'), mention_author=True)
            
    @commands.command(description="Send a picture of Danny.", brief="Send a picture of Danny")
    async def danny(self, ctx):
        dir = f"I:\\Danny Infinitum"
        file_name = random.choice(os.listdir(dir))
        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'danny.png'), mention_author=True)
            
    @commands.command(description="Display file counts for key directories in Dannybot", brief="Display file counts for key directories in Dannybot")
    async def db(self, ctx):

        embed = discord.Embed(title="Dannybot File Totals", color=0xf77e9a)
        embed.add_field(name="Pooter Files:", value=str(str(fileCount(f"{dannybot}\\database\\Pooter")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Pooter"))), inline=True)
        embed.add_field(name="Danny Files:", value=str(str(fileCount(f"I:\\Danny Infinitum")) + " files \n" + str(fileSize(f"I:\\Danny Infinitum"))), inline=True)
        embed.add_field(name="Leffrey Files:", value=str(str(fileCount(f"{dannybot}\\database\\Leffrey")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Leffrey"))), inline=True)
        embed.add_field(name="Femboy Files:", value=str(str(fileCount(f"{dannybot}\\database\\Femboy")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Femboy"))), inline=True)
        embed.add_field(name="Fanboy Files:", value=str(str(fileCount(f"{dannybot}\\database\\Fanboy")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Fanboy"))), inline=True)
        embed.add_field(name="Glass Cup Images:", value=str(str(fileCount(f"{dannybot}\\database\\Glasscup")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Glasscup"))), inline=True)
        embed.add_field(name="Plastic Cup Images:", value=str(str(fileCount(f"{dannybot}\\database\\Plasticcup")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Plasticcup"))), inline=True)
        embed.add_field(name="Burger Files:", value=str(str(fileCount(f"{dannybot}\\database\\Burger")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Burger"))), inline=True)
        embed.add_field(name="Nekopara Files:", value=str(str(fileCount(NekoparaPath)) + " files \n" + str(fileSize(NekoparaPath))), inline=True)
        embed.add_field(name="Animal Girl Images:", value=str(str(fileCount(f"{dannybot}\\database\\Mimi")) + " files \n" + str(fileSize(f"{dannybot}\\database\\Mimi"))), inline=True)
        embed.add_field(name="Video Files:", value=str(str(fileCount(VideosPath)) + " files \n" + str(fileSize(VideosPath))), inline=True)
        embed.add_field(name="Image Files:", value=str(str(fileCount(PicturesPath)) + " files \n" + str(fileSize(PicturesPath))), inline=True)
        embed.add_field(name="GIF Files:", value=str(str(fileCount(GifsPath)) + " files \n" + str(fileSize(GifsPath))), inline=True)

        await ctx.reply(embed=embed, mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))

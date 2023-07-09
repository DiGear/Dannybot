# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='neko', aliases=['catgirl'], description="Send a picture of an catgirl using the nekos.life API.", brief="Send a picture of an catgirl")
    async def neko(self, ctx: commands.Context):
        try:
            api_response = requests.get("https://nekos.life/api/v2/img/neko")
            api_response.raise_for_status()  # Raise an exception if the API request was not successful
            data = api_response.json()
            image_url = data.get("url")

            if image_url:
                await ctx.reply(image_url, mention_author=True)
            else:
                await ctx.send("Failed to retrieve catgirl image.")
        except requests.exceptions.RequestException:
            return
        
    @commands.hybrid_command(name="img", description="Send a random picture or file from a category.", brief="Send a random picture or file from a category")
    async def imgcmd(self, ctx: commands.Context, category: Literal['mimi', 'nekopara', 'vid', 'img', 'leffrey', 'gif', 'femboy', 'fanboy', 'glasscup', 'plasticcup', 'burger', 'danny'] = 'img'):
        await ctx.defer()
        file_types = {
            "mimi": MimiPath,
            "nekopara": NekoparaPath,
            "vid": VideosPath,
            "img": PicturesPath,
            "leffrey": f"{dannybot}\\database\\Leffrey",
            "gif": GifsPath,
            "femboy": f"{dannybot}\\database\\Femboy",
            "fanboy": f"{dannybot}\\database\\Fanboy",
            "glasscup": f"{dannybot}\\database\\Glasscup",
            "plasticcup": f"{dannybot}\\database\\Plasticcup",
            "burger": f"{dannybot}\\database\\Burger",
            "danny": f"I:\\Danny Infinitum"
        }
        if category not in file_types:
            await ctx.reply("Invalid category. Please choose from: " + ", ".join(file_types.keys()))
            return
        dir = file_types[category]
        file_name = random.choice(os.listdir(dir))
        with open(f"{dir}\\{file_name}", "rb") as f:
            await ctx.reply(file=File(f, "img.png"), mention_author=True)
        
    @commands.hybrid_command(name="database", aliases=['db', 'databases', 'dbs'], description="Display file counts for key directories in Dannybot", brief="Display file counts for key directories in Dannybot")
    async def db(self, ctx):
        # Define directory paths
        pooter_path = f"{dannybot}\\database\\Pooter"
        danny_path = "I:\\Danny Infinitum"
        leffrey_path = f"{dannybot}\\database\\Leffrey"
        femboy_path = f"{dannybot}\\database\\Femboy"
        fanboy_path = f"{dannybot}\\database\\Fanboy"
        glasscup_path = f"{dannybot}\\database\\Glasscup"
        plasticcup_path = f"{dannybot}\\database\\Plasticcup"
        burger_path = f"{dannybot}\\database\\Burger"
        nekopara_path = NekoparaPath
        animalgirl_path = f"{dannybot}\\database\\Mimi"
        video_path = VideosPath
        image_path = PicturesPath
        gif_path = GifsPath

        # Create the embed
        embed = discord.Embed(title="Dannybot File Totals", color=0xf77e9a)

        # Add fields to the embed
        embed.add_field(name="Pooter Files:", value=f"{fileCount(pooter_path)} files\n{fileSize(pooter_path)}")
        embed.add_field(name="Danny Files:", value=f"{fileCount(danny_path)} files\n{fileSize(danny_path)}")
        embed.add_field(name="Leffrey Files:", value=f"{fileCount(leffrey_path)} files\n{fileSize(leffrey_path)}")
        embed.add_field(name="Femboy Files:", value=f"{fileCount(femboy_path)} files\n{fileSize(femboy_path)}")
        embed.add_field(name="Fanboy Files:", value=f"{fileCount(fanboy_path)} files\n{fileSize(fanboy_path)}")
        embed.add_field(name="Glass Cup Images:", value=f"{fileCount(glasscup_path)} files\n{fileSize(glasscup_path)}")
        embed.add_field(name="Plastic Cup Images:", value=f"{fileCount(plasticcup_path)} files\n{fileSize(plasticcup_path)}")
        embed.add_field(name="Burger Files:", value=f"{fileCount(burger_path)} files\n{fileSize(burger_path)}")
        embed.add_field(name="Nekopara Files:", value=f"{fileCount(nekopara_path)} files\n{fileSize(nekopara_path)}")
        embed.add_field(name="Animal Girl Images:", value=f"{fileCount(animalgirl_path)} files\n{fileSize(animalgirl_path)}")
        embed.add_field(name="Video Files:", value=f"{fileCount(video_path)} files\n{fileSize(video_path)}")
        embed.add_field(name="Image Files:", value=f"{fileCount(image_path)} files\n{fileSize(image_path)}")
        embed.add_field(name="GIF Files:", value=f"{fileCount(gif_path)} files\n{fileSize(gif_path)}")

        await ctx.reply(embed=embed, mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))
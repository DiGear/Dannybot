# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="neko",
        aliases=["catgirl"],
        description="Send a picture of an catgirl using the nekos.life API.",
        brief="Send a picture of an catgirl",
    )
    async def neko(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/neko") as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("url")

                    if image_url:
                        await ctx.reply(image_url, mention_author=True)
                    else:
                        await ctx.send("Failed to retrieve catgirl image.")
                        
    @commands.hybrid_command(
        name="pizzi",
        description="Emulate Pizzi messages using textgenrnn.",
        brief="Emulate Pizzi using AI",
    )
    async def pizzi(self, ctx: commands.Context):
        await ctx.defer()
        def generate_pizzi_text():
            temperature = round(random.uniform(0.01, 1.5), 2)
            textgen_2 = textgenrnn(f"{dannybot}\\assets\\textgenrnn\\pizzi.hdf5")
            output_buffer = StringIO()
            sys.stdout = output_buffer
            try:
                textgen_2.generate(1, temperature=temperature)
            finally:
                sys.stdout = sys.__stdout__
            captured_output = output_buffer.getvalue()
            return captured_output.strip().splitlines()[-1]
        pizzi_text = generate_pizzi_text()
        pizzi_image = random.choice(os.listdir(f"{dannybot}\\database\\dooter\\"))
        with open(f"{dannybot}\\database\\dooter\\{pizzi_image}", "rb") as f:
            await ctx.reply(pizzi_text, file=File(f, "pizzi.png"))
                        
    @commands.command(hidden=True)
    async def po(self, ctx):
        file_name = random.choice(os.listdir(f"{dannybot}\\database\\Po\\"))
        with open(f"{dannybot}\\database\\Po\\{file_name}", "rb") as f:
            await ctx.reply(file=File(f, "img.png"), mention_author=True)

    @commands.hybrid_command(
        name="img",
        description="Send a random picture or file from a category.",
        brief="Send a random picture or file from a category",
    )
    async def imgcmd(
        self,
        ctx: commands.Context,
        category: Literal[
            "mimi",
            "nekopara",
            "vid",
            "img",
            "leffrey",
            "gif",
            "femboy",
            "fanboy",
            "glasscup",
            "plasticcup",
            "burger",
            "danny",
        ] = "img",
    ):
        await ctx.defer()
        file_types = {
            "mimi": f"{dannybot}\\database\\Mimi",
            "nekopara": f"{dannybot}\\database\\Nekopara",
            "vid": f"{dannybot}\\database\\Vid",
            "img": f"{dannybot}\\database\\Img",
            "leffrey": f"{dannybot}\\database\\Leffrey",
            "gif": f"{dannybot}\\database\\Gif",
            "femboy": f"{dannybot}\\database\\Femboy",
            "fanboy": f"{dannybot}\\database\\Fanboy",
            "glasscup": f"{dannybot}\\database\\Glasscup",
            "plasticcup": f"{dannybot}\\database\\Plasticcup",
            "burger": f"{dannybot}\\database\\Burger",
            "danny": f"{dannybot}\\database\\Danny",
        }
        if category not in file_types:
            await ctx.reply(
                "Invalid category. Please choose from: " + ", ".join(file_types.keys())
            )
            return
        dir = file_types[category]
        file_name = random.choice(os.listdir(dir))
        with open(f"{dir}\\{file_name}", "rb") as f:
            await ctx.reply(file=File(f, "img.png"), mention_author=True)

    @commands.hybrid_command(
        name="database",
        aliases=["db", "databases", "dbs"],
        description="Display file counts for key directories in Dannybot",
        brief="Display file counts for key directories in Dannybot",
    )
    async def db(self, ctx):
        # Define directory paths in a dictionary
        directory_paths = {
            "Pooter Files:": f"{dannybot}\\database\\Pooter",
            "Danny Files:": f"{dannybot}\\database\\Danny",
            "Leffrey Files:": f"{dannybot}\\database\\Leffrey",
            "Femboy Files:": f"{dannybot}\\database\\Femboy",
            "Fanboy Files:": f"{dannybot}\\database\\Fanboy",
            "Glass Cup Images:": f"{dannybot}\\database\\Glasscup",
            "Plastic Cup Images:": f"{dannybot}\\database\\Plasticcup",
            "Burger Files:": f"{dannybot}\\database\\Burger",
            "Nekopara Files:": f"{dannybot}\\database\\Nekopara",
            "Animal Girl Images:": f"{dannybot}\\database\\Mimi",
            "Video Files:": f"{dannybot}\\database\\Vid",
            "Image Files:": f"{dannybot}\\database\\Img",
            "GIF Files:": f"{dannybot}\\database\\Gif",
        }

        # Create the embed
        embed = discord.Embed(title="Dannybot File Totals", color=0xF77E9A)

        # Add fields to the embed
        for name, path in directory_paths.items():
            embed.add_field(
                name=name, value=f"{fileCount(path)} files\n{fileSize(path)}"
            )

        await ctx.reply(embed=embed, mention_author=True)
    
    @commands.command()
    @commands.is_owner()
    async def kill(self, ctx, user: discord.User):
        def is_user(m):
            return m.author == user
        deleted = await ctx.channel.purge(check=is_user, bulk=True)
        await ctx.send(f'Deleted {len(deleted)} messages from {user.mention}')


async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))

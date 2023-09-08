# huh

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class secret(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def taur_add(
        self, ctx, file_url: typing.Optional[str] = "File_Is_Attachment"
    ):
        whitelist = [206392667351941121, 343224184110841856]  # Whitelisted user IDs

        if ctx.author.id not in whitelist:
            await ctx.send("You are not whitelisted for this command!")
            return

        if file_url == "File_Is_Attachment":
            if not ctx.message.attachments:
                await ctx.send("No file attached.")
                return

            link_to_file = ctx.message.attachments[0].url
        else:
            link_to_file = file_url

        await ctx.send("Downloading...", delete_after=5)

        # Download the image file and save it to the specified directory
        file_path = f"{dannybot}\\database\\Taurs\\{randhex(64)}.png"
        response = requests.get(link_to_file)

        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            await ctx.send("File downloaded!", delete_after=5)
        else:
            await ctx.send("Failed to download the file.")

    @commands.command(hidden=True)
    async def taur(self, ctx):
        dir = f"{dannybot}\\database\\Taurs"
        file_name = random.choice(os.listdir(dir))
        with open(f"{dir}\\{file_name}", "rb") as f:
            await ctx.reply(file=File(f, "Taur.png"), mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(secret(bot))

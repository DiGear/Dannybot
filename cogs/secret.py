# huh

# if you can't find a variable used in this file its probably imported from here
from config import *


class secret(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def poopoo(self, ctx):
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))
        pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
        with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
            await ctx.reply(file=File(f, pooter_file))

    @commands.command(hidden=True)
    async def taur_add(self, ctx, File_Url: typing.Optional[str] = "File_Is_Attachment"):
        whitelist = [206392667351941121, 343224184110841856] # hardcoded whitelist lol lmao
        if not ctx.author.id in whitelist:
            await ctx.send("You are not whitelisted for this command!")
            return
        else:
            if(File_Url == "File_Is_Attachment"):
                Link_To_File = ctx.message.attachments[0].url
            else:
                Link_To_File = File_Url
            await ctx.send("Downloading...", delete_after=5)

            filename = randhex(64)

            # this code block writes the image data to a file
            with open(f"{dannybot}\\database\\Taurs\\{filename}.png", 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
            await ctx.send("File Downloaded!", delete_after=5)

    @commands.command(hidden=True)
    async def taur(self, ctx):
        dir = f"{dannybot}\\database\\Taurs"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'Taur.png'), mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(secret(bot))
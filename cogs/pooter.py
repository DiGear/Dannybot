#fuick
from config import *

logger = logging.getLogger(__name__)

# Initialize BagRandom instances for pooter and dooter
bag_random_pooter = BagRandom('pooter_bag.json')
bag_random_dooter = BagRandom('dooter_bag.json')

class Pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pooter_db_path = os.path.join(dannybot, "database", "Pooter")
        self.dooter_db_path = os.path.join(dannybot, "database", "Dooter")
        
        # Initialize the pooter bag if it doesn't exist
        if not 'pooter' in bag_random_pooter.bags:
            pooter_files = os.listdir(self.pooter_db_path)
            bag_random_pooter.create_bag('pooter', pooter_files)
        
        # Initialize the dooter bag if it doesn't exist
        if not 'dooter' in bag_random_dooter.bags:
            dooter_files = os.listdir(self.dooter_db_path)
            bag_random_dooter.create_bag('dooter', dooter_files)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not any(msg.content.startswith(f"{pfx}poo") for pfx in dannybot_prefixes):
            return

        if msg.guild.id not in whitelist:
            await msg.channel.send("This server is not whitelisted for this command.")
            return

        poo_count = msg.content.count("poo")

        if poo_count == 1:
            return

        for _ in range(poo_count):
            img_file = bag_random_pooter.choice('pooter')
            with open(os.path.join(self.pooter_db_path, img_file), "rb") as img:
                await msg.channel.send(file=discord.File(img), reference=msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        async def download_file(url, count, message, file_name):
            guild = self.bot.get_guild(payload.guild_id)
            if guild.id not in whitelist:
                await message.send("This server is not whitelisted for this command.")
                return
            tenor = False
            if any(ext.lower() in url for ext in database_acceptedFiles):
                if "https://tenor.com/view/" in url:
                    tenor = True
                    tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", url).group(1)
                    url = gettenor(tenor_id)
                if input_message.attachments:
                    total_files = len(input_message.attachments)
                else:
                    total_files = 1
                if not tenor:
                    file_url = url.split("?")
                    file_extension = file_url[0].split(".")[-1]
                    file_url = f"{file_url[0]}?{file_url[1]}"
                else:
                    file_url = url
                    file_extension = file_url.split(".")[-1]
                file_name = f"{randhex(128)}.{file_extension}"
                file_path = f"{dannybot}/database/Pooter/{file_name}"

                with open(file_path, "wb") as f:
                    f.write(requests.get(url).content)

                bag_random_pooter.add_values('pooter', [file_name])
                downloaded_files.add(url)
                await self.bot.get_channel(logs_channel).send(
                    f"{payload.member.global_name} ({payload.member.id}) has pootered: {url}"
                )
                return True
            await message.send(
                "This file is not a valid image or video file!", delete_after=3
            )
            await input_message.add_reaction("⚠️")
            return False

        message_channel = self.bot.get_channel(payload.channel_id)
        input_message = await message_channel.fetch_message(payload.message_id)

        if payload.member.id == 343224184110841856 and str(payload.emoji)[0] == "🔖":
            await self.bot.get_channel(bookmarks_channel).send(input_message.jump_url)
            await input_message.remove_reaction("🔖", payload.member)
        elif str(payload.emoji)[0] == "💩":
            files = input_message.attachments or [input_message.content.strip()]
            tasks = []
            for idx, file in enumerate(files):
                if hasattr(file, "url"):
                    file_url = file.url.split("?")
                    file_extension = file_url[0].split(".")[-1]
                    file_url = f"{file_url[0]}?{file_url[1]}"
                    sanitized_filename = sanitize_filename(file_url) + "." + file_extension
                else:
                    file_url = file
                    file_extension = file.split(".")[-1]
                    sanitized_filename = sanitize_filename(file) + "." + file_extension

                task = asyncio.create_task(
                    download_file(
                        file_url, idx + 1, message_channel, sanitized_filename
                    )
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            if all(results):
                await input_message.add_reaction("✅")
            await input_message.remove_reaction("💩", payload.member)

    @commands.command(
        hidden=True,
        aliases=["poo", "poop", ":spoon:", "🥄", "💩"],
        description="Send or receive a file from a user-built archive of files.",
        brief="Send/Receive files from a public archive.",
    )
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        async def download_file(url, current_download):
            if ctx.guild.id not in whitelist:
                await ctx.send("This server is not whitelisted for this command.")
                return
            tenor = False
            if any(ext.lower() in url for ext in database_acceptedFiles):
                if "https://tenor.com/view/" in url:
                    tenor = True
                    tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", url).group(1)
                    url = gettenor(tenor_id)
                if not tenor:
                    file_url = url.split("?")
                    file_extension = file_url[0].split(".")[-1]
                    file_url = f"{file_url[0]}?{file_url[1]}"
                else:
                    file_url = url
                    file_extension = file_url.split(".")[-1]
                file_name = f"{randhex(128)}.{file_extension}"
                file_path = f"{dannybot}/database/Pooter/{file_name}"

                with open(file_path, "wb") as f:
                    f.write(requests.get(url).content)

                bag_random_pooter.add_values('pooter', [file_name])
                downloaded_files.add(url)
                if len(downloaded_files) == total_downloads:
                    await ctx.message.add_reaction("✅")
                await self.bot.get_channel(logs_channel).send(
                    f"{ctx.author.global_name} ({ctx.author.id}) has pootered: {url}"
                )
            else:
                await ctx.send("Invalid image or video file!", delete_after=3)
                await ctx.message.add_reaction("⚠️")
                return

        downloads = 1
        f_name = randhex(128)
        downloaded_files = set()
        total_downloads = 0
        if ctx.message.attachments:
            total_downloads = len(ctx.message.attachments)
            tasks = []
            for i, attachment in enumerate(ctx.message.attachments):
                file_url = attachment.url.split("?")
                file_extension = file_url[0].split(".")[-1]
                file_url = f"{file_url[0]}?{file_url[1]}"
                filename = f"{randhex(128)}.{file_extension}"
                task = asyncio.create_task(download_file(file_url, i + 1))
                tasks.append(task)
            await asyncio.gather(*tasks)
        elif not File_Url:
            if ctx.guild.id not in whitelist:
                return
            pooter_file = bag_random_pooter.choice('pooter')
            with open(os.path.join(self.pooter_db_path, pooter_file), "rb") as f:
                await ctx.reply(file=discord.File(f, pooter_file))
        else:
            total_downloads = 1
            await download_file(File_Url, 1)

    @commands.command(hidden=True)
    async def dooter(self, ctx, File_Url: typing.Optional[str] = None):
        async def download_file(url, current_download):
            if ctx.author.id != 305161653463285780:
                await ctx.send("You are not whitelisted for this command.")
                return
            tenor = False
            if any(ext.lower() in url for ext in database_acceptedFiles):
                if "https://tenor.com/view/" in url:
                    tenor = True
                    tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", url).group(1)
                    url = gettenor(tenor_id)
                if not tenor:
                    file_url = url.split("?")
                    file_extension = file_url[0].split(".")[-1]
                    file_url = f"{file_url[0]}?{file_url[1]}"
                else:
                    file_url = url
                    file_extension = file_url.split(".")[-1]
                file_name = f"{randhex(128)}.{file_extension}"
                file_path = f"{dannybot}/database/Dooter/{file_name}"

                with open(file_path, "wb") as f:
                    f.write(requests.get(url).content)

                bag_random_dooter.add_values('dooter', [file_name])
                downloaded_files.add(url)
                if len(downloaded_files) == total_downloads:
                    await ctx.message.add_reaction("✅")
                await self.bot.get_channel(logs_channel).send(
                    f"{ctx.author.global_name} ({ctx.author.id}) has dootered: {url}"
                )
            else:
                await ctx.send("Invalid image or video file!", delete_after=3)
                await ctx.message.add_reaction("⚠️")
                return

        downloads = 1
        f_name = randhex(128)
        downloaded_files = set()
        total_downloads = 0
        if ctx.message.attachments:
            total_downloads = len(ctx.message.attachments)
            tasks = []
            for i, attachment in enumerate(ctx.message.attachments):
                file_url = attachment.url.split("?")
                file_extension = file_url[0].split(".")[-1]
                file_url = f"{file_url[0]}?{file_url[1]}"
                filename = f"{randhex(128)}.{file_extension}"
                task = asyncio.create_task(download_file(file_url, i + 1))
                tasks.append(task)
            await asyncio.gather(*tasks)
        else:
            total_downloads = 1
            await download_file(File_Url, 1)

async def setup(bot: commands.Bot):
    await bot.add_cog(Pooter(bot))
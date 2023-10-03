# this is most likely gonna be necessary for expanding upon pooter later

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        clean_pooter_silent()

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # Check if the message starts with any of the bot prefixes
        if not any(msg.content.startswith(f"{pfx}poo") for pfx in dannybot_prefixes):
            return

        # Count the occurrences of "poo" in the message
        poo_count = msg.content.count("poo")

        # Define the path to the Pooter database folder
        pooter_db_path = os.path.join(
            dannybot, "database", "Pooter"
        )  # this is literally pointless i just thought it was neat you could do it this way

        # If there is only one occurrence of "poo", do nothing
        if poo_count == 1:
            return

        # Send multiple random images from the Pooter database based on poo_count
        for _ in range(poo_count):
            # Select a random image file from the Pooter database folder
            img_file = random.choice(os.listdir(pooter_db_path))
            with open(os.path.join(pooter_db_path, img_file), "rb") as img:
                # Send the image as a file in the same channel as the original message
                await msg.channel.send(file=discord.File(img), reference=msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Function to download a file from a URL
        async def download_file(url, count, message, file_name):
            if any(ext in url.lower() for ext in database_acceptedFiles):
                if "https://tenor.com/view/" in url:
                    tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", url).group(1)
                    url = gettenor(tenor_id)
                if input_message.attachments:
                    total_files = len(input_message.attachments)
                else:
                    total_files = 1
                await message.send(
                    f"Downloading... {count} of {total_files}", delete_after=1
                )
                file_url = url.split("?")[0]
                file_extension = file_url.split(".")[-1]
                with open(
                    f"{dannybot}/database/Pooter/{randhex(128)}.{file_extension}", "wb"
                ) as f:
                    f.write(requests.get(url).content)
                await self.bot.get_channel(logs_channel).send(
                    f"{payload.member.global_name} ({payload.member.id}) has pootered: {url}"
                )
                return True
            await message.send(
                "This file is not a valid image or video file!", delete_after=3
            )
            await input_message.add_reaction("⚠️")
            return False

        # Get the message channel and input message
        message_channel = self.bot.get_channel(payload.channel_id)
        input_message = await message_channel.fetch_message(payload.message_id)

        # Check if the reaction is from a specific user and emoji
        if payload.member.id == 343224184110841856 and str(payload.emoji)[0] == "🔖":
            # Send the message URL to bookmarks_channel and remove the reaction
            await self.bot.get_channel(bookmarks_channel).send(input_message.jump_url)
            await input_message.remove_reaction("🔖", payload.member)
        elif str(payload.emoji)[0] == "💩":
            # Get a list of files to download (attachments or message content)
            files = input_message.attachments or [input_message.content.strip()]

            # Create tasks to download each file concurrently
            tasks = []
            for idx, file in enumerate(files):
                if hasattr(file, "url"):
                    file_url = file.url.split("?")[0]
                    file_extension = file_url.split(".")[-1]
                    sanitized_filename = (
                        sanitize_filename(file_url) + "." + file_extension
                    )
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
            # Gather the results of the download tasks
            results = await asyncio.gather(*tasks)

            # If all downloads are successful, add a checkmark reaction
            if all(results):
                await input_message.add_reaction("✅")

            # Remove the poop emoji reaction from the user
            await input_message.remove_reaction("💩", payload.member)

    @commands.command(
        hidden=True,
        aliases=["poo", "poop", ":spoon:", "🥄"],
        description="Send or receive a file from a user-built archive of files. You can upload 10 files at a time, or not attach any files to view the archive instead.",
        brief="Send/Receive files from a public archive.",
    )
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        async def download_file(url, current_download):
            # Check if the file format is valid
            if not any(ext in url for ext in database_acceptedFiles):
                await ctx.send("Invalid image or video file!", delete_after=3)
                await ctx.message.add_reaction("⚠️")
                return
            if "https://tenor.com/view/" in url:
                tenor_id = re.search(r"tenor\.com/view/.*-(\d+)", url).group(1)
                url = gettenor(tenor_id)
            # Display download progress
            await ctx.send(
                f"Downloading... {current_download} of {total_downloads}",
                delete_after=1,
            )
            file_url = url.split("?")[0]
            file_extension = file_url.split(".")[-1]
            with open(
                f"{dannybot}/database/Pooter/{randhex(128)}.{file_extension}", "wb"
            ) as f:
                f.write(requests.get(url).content)
            # Track downloaded files and check if all downloads are complete
            downloaded_files.add(url)
            # React with a checkpoint when all files download successfully
            if len(downloaded_files) == total_downloads:
                await ctx.message.add_reaction("✅")
            # Log the download action
            await self.bot.get_channel(logs_channel).send(
                f"{ctx.author.global_name} ({ctx.author.id}) has pootered: {url}"
            )

        downloads = 1
        f_name = randhex(128)
        downloaded_files = set()  # Initialize a set to track downloaded files
        total_downloads = 0  # Initialize total_downloads here
        if ctx.message.attachments:
            total_downloads = len(ctx.message.attachments)
            tasks = []
            for i, attachment in enumerate(ctx.message.attachments):
                file_url = attachment.url.split("?")[0]
                file_extension = file_url.split(".")[-1]
                filename = f"{randhex(128)}.{file_extension}"
                task = asyncio.create_task(download_file(file_url, i + 1))
                tasks.append(task)
            await asyncio.gather(*tasks)
        elif not File_Url:
            # If no attachment or File_Url provided, select a random file from the archive
            pooter_files = os.listdir(f"{dannybot}/database/Pooter/")
            pooter_file = random.choice(pooter_files)
            with open(f"{dannybot}/database/Pooter/{pooter_file}", "rb") as f:
                await ctx.reply(file=discord.File(f, pooter_file))
        else:
            total_downloads = 1  # Initialize total_downloads to 1 for links
            # Download the file specified in File_Url
            await download_file(File_Url, 1)


async def setup(bot: commands.Bot):
    await bot.add_cog(pooter(bot))

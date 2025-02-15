# fuick
from config import *

logger = logging.getLogger(__name__)

# Initialize BagRandom instances for pooter and dooter
bag_random_pooter = BagRandom("pooter_bag.json")
bag_random_dooter = BagRandom("dooter_bag.json")


class Pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pooter_db_path = os.path.join(dannybot, "database", "Pooter")
        self.pooter_quiz_db_path = os.path.join(dannybot, "database", "Pooterquiz")
        self.dooter_db_path = os.path.join(dannybot, "database", "Dooter")

        # Initialize the pooter bag if it doesn't exist
        if not "pooter" in bag_random_pooter.bags:
            pooter_files = os.listdir(self.pooter_db_path)
            bag_random_pooter.create_bag("pooter", pooter_files)

        # Initialize the dooter bag if it doesn't exist
        if not "dooter" in bag_random_dooter.bags:
            dooter_files = os.listdir(self.dooter_db_path)
            bag_random_dooter.create_bag("dooter", dooter_files)

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
            img_file = bag_random_pooter.choice("pooter")
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
                file_name = (
                    f"pooterquiz_{payload.member.id}_{randhex(64)}.{file_extension}"
                )
                file_path = f"{dannybot}/database/Pooter/{file_name}"

                with open(file_path, "wb") as f:
                    f.write(requests.get(url).content)

                bag_random_pooter.add_values("pooter", [file_name])
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
            results = await asyncio.gather(*tasks)
            if all(results):
                await input_message.add_reaction("✅")
            await input_message.remove_reaction("💩", payload.member)

    @commands.command(
        aliases=["poo", "poop", ":spoon:", "🥄", "💩"],
        description="Send or receive a file from a user-built archive of files.",
        brief="Send/Receive files from a public archive.",
    )
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        async def download_file(url, current_download):
            if (
                ctx.guild is not None and ctx.guild.id not in whitelist
            ) and ctx.author.id != bot.owner_id:
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
                file_name = f"pooterquiz_{ctx.author.id}_{randhex(64)}.{file_extension}"
                file_path = f"{dannybot}/database/Pooter/{file_name}"

                with open(file_path, "wb") as f:
                    f.write(requests.get(url).content)

                bag_random_pooter.add_values("pooter", [file_name])
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
                filename = f"pooterquiz_{ctx.author.id}_{randhex(64)}.{file_extension}"
                task = asyncio.create_task(download_file(file_url, i + 1))
                tasks.append(task)
            await asyncio.gather(*tasks)
        elif not File_Url:
            if (
                ctx.guild is not None and ctx.guild.id not in whitelist
            ) and ctx.author.id != bot.owner_id:
                return
            pooter_file = bag_random_pooter.choice("pooter")
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

                bag_random_dooter.add_values("dooter", [file_name])
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

    def load_history(self, history_file_path):
        if os.path.exists(history_file_path):
            with open(history_file_path, 'r') as f:
                return json.load(f)
        else:
            return []

    def save_history(self, history_file_path, history):
        with open(history_file_path, 'w') as f:
            json.dump(history, f, indent=4)

    @commands.hybrid_command(alisess=["pooquiz", "wpi"])
    async def pooterquiz(self, ctx):
        pooter_db_path = self.pooter_db_path
        pooter_quiz_db_path = self.pooter_quiz_db_path
        history_file_path = f"{dannybot}\\assets\\pooterquiz_history.json"
        all_files = os.listdir(pooter_db_path) + os.listdir(pooter_quiz_db_path)
        excluded_extensions = {".mp4", ".webm", ".mov"}
        quiz_files = [
            f
            for f in all_files
            if f.startswith("pooterquiz_")
            and os.path.splitext(f)[1].lower() not in excluded_extensions
        ]
        if not quiz_files:
            await ctx.send("shit is fucked")
            return

        history = self.load_history(history_file_path)

        id_counts = {}
        for file in quiz_files:
            match = re.match(r"pooterquiz_(\d+)_", file)
            if match:
                user_id = match.group(1)
                id_counts[user_id] = id_counts.get(user_id, 0) + 1

        def weight(count):
            ranges = [(10, (0.05, 0.1)), (100, (0.1, 0.15)), (1000, (0.4, 0.5)),
                    (2000, (0.15, 0.2)), (5000, (0.1, 0.15))]
            
            for max_count, prob_range in ranges:
                if count <= max_count:
                    return random.uniform(*prob_range)
            return random.uniform(0.05, 0.07)

        weighted_files = []
        for file in quiz_files:
            match = re.match(r"pooterquiz_(\d+)_", file)
            if match:
                user_id = match.group(1)
                weight_value = weight(id_counts[user_id])
                weighted_files.extend([file] * int(weight_value * 1000))

        if not weighted_files:
            await ctx.send("no valid quiz files after weighting")
            return

        # keep rerolling until we get a file not in the last 250
        while True:
            chosen_file = random.choice(weighted_files)

            if chosen_file not in history:
                break
            else:
                continue

        history.append(chosen_file)
        if len(history) > 5000:
            history.pop(0)

        self.save_history(history_file_path, history)

        if chosen_file in os.listdir(self.pooter_db_path):
            file_path = os.path.join(self.pooter_db_path, chosen_file)
        else:
            file_path = os.path.join(self.pooter_quiz_db_path, chosen_file)

        match = re.match(r"pooterquiz_(\d+)_", chosen_file)
        if not match:
            await ctx.send("shit is fucked again")
            return
        target_id = int(match.group(1))

        target_user = self.bot.get_user(target_id)
        if target_user is None:
            try:
                target_user = await self.bot.fetch_user(target_id)
            except Exception as e:
                await ctx.send("idk who submitted this lol")
                print(f"Error fetching user {target_id}: {e}")
                return

        member = ctx.guild.get_member(target_id) if ctx.guild else None

        allowed_answers = {target_user.name.lower()}
        if member and member.display_name:
            allowed_answers.add(member.display_name.lower())

        users_dict = {
            "343224184110841856": ["danny", "fdg", "digear"],
            "158418656861093888": ["flashlight", "ezogaming", "ezo"],
            "422249760876003328": ["flashlight", "ezogaming", "ezo"],
            "305161653463285780": ["pizzi"],
            "243104841021390859": ["crypted"],
            "249411048518451200": ["rotty"],
            "229401113382617088": ["leffrey", "leif"],
            "211419370860183552": ["cris", "crys", "crystal"],
            "327207076067803156": ["scroogily man", "isaac"],
            "569267645707321344": ["jordi"],
            "206392667351941121": ["sam", "sam deluxe"],
            "588539600428072971": ["incine"],
            "538112945800871938": ["reese", "videogame71", "joycons"],
            "285049524068810762": ["outerspacepirate", "outer", "osp", "sean", "shawn"],
            "229396708201594881": ["indev", "devin"],
            "114112473430360070": ["kneecap", "viath"],
            "419715716770562078": ["momentum", "mom"],
            "299907871640911872": ["maki", "maki ligon"],
            "588342367476776961": ["maki", "maki ligon"],
            "519202056846704680": ["chris", "chris j"],
            "847276836172988426": ["dannybot"],
            "246131844859297800": ["neatcrown", "neat"],
            "176084654850310145": ["ben", "ben3759"],
            "562369969879253054": ["gilbert", "liam"],
            "203882027366350859": ["bravo"],
        }

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Pooter Quiz",
            description="Who Pootered this file? (answer in chat within 30 seconds)",
        )
        embed.set_image(url=f"attachment://{chosen_file}")

        file_attachment = discord.File(file_path, filename=chosen_file)
        botmessage = await ctx.reply(embed=embed, file=file_attachment, mention_author=True)

        def check(message):
            return message.channel == botmessage.channel and message.author == ctx.message.author and message.author != self.bot.user

        try:
            response = await self.bot.wait_for("message", timeout=30.0, check=check)
            response_content = response.content.strip().lower()

            if str(target_id) in users_dict:
                if any(fuzz.partial_ratio(response_content.lower(), name.lower()) >= 80 for name in users_dict[str(target_id)]):
                    await ctx.send(f"epic win **(you gained 10 DP)**")
                    addxp_command = self.bot.get_command('addxp')
                    await ctx.invoke(addxp_command, xp=10)
                    return
                else:
                    correct_names = ", ".join(users_dict[str(target_id)])
                    await ctx.send(
                        f"wrong answer, {response.author.mention}\nthe correct answer(s) would have been **{correct_names}**."
                    )
                    return
            else:
                await ctx.send(f"add {target_user.name} ({target_user.id}) to the users_dict")

        except asyncio.TimeoutError:
            correct_names = ", ".join(users_dict[str(target_id)])
            await ctx.send(f"times up, {ctx.message.author.mention}\nthe correct answer(s) would have been **{correct_names}**.")
            return
        except asyncio.CancelledError:
            await ctx.send("the quiz was cancelled")
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(Pooter(bot))

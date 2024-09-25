# primarily the database related commands

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)
bag_random_dooter = BagRandom('dooter_bag.json')

class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.file_paths = {
            "mimi": f"{dannybot}\\database\\Mimi",
            "nekopara": f"{dannybot}\\database\\Nekopara",
            "leffrey": f"{dannybot}\\database\\Leffrey",
            "femboy": f"{dannybot}\\database\\Femboy",
            "fanboy": f"{dannybot}\\database\\Fanboy",
            "glasscup": f"{dannybot}\\database\\Glasscup",
            "plasticcup": f"{dannybot}\\database\\Plasticcup",
            "burger": f"{dannybot}\\database\\Burger",
            "danny": f"{dannybot}\\database\\Danny",
        }

        # Initialize BagRandom instances for each category except 'dooter'
        self.bags = {category: BagRandom(f'{category}_bag.json') for category in self.file_paths if category != "dooter"}
        
        # Generate bags if they don't exist
        self.initialize_bags()

    def initialize_bags(self):
        """Generate bags if they don't already exist."""
        for category, path in self.file_paths.items():
            if category != "dooter":  # Skip the 'dooter' category
                if category not in self.bags[category].bags:
                    if os.path.exists(path):
                        files = os.listdir(path)
                        self.bags[category].create_bag(category, files)
                    else:
                        print(f"Directory for category '{category}' does not exist: {path}")

    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.hybrid_command(
        name="neko",
        aliases=["catgirl"],
        description="Send a picture of an catgirl using the nekos.life API.",
        brief="Send a picture of an catgirl",
    )
    async def neko(self, ctx: commands.Context):
        if (ctx.guild is not None and ctx.guild.id not in whitelist) and ctx.author.id != bot.owner_id:
            await ctx.send("This server is not whitelisted for this command.")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/neko") as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("url")

                    if image_url:
                        await ctx.reply(image_url, mention_author=True)
                    else:
                        await ctx.send("Failed to retrieve catgirl image.")

    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.hybrid_command(
        name="pizzi",
        description="Emulate Pizzi messages using textgenrnn.",
        brief="Emulate Pizzi using AI",
    )
    async def pizzi(self, ctx: commands.Context, temperature: typing.Optional[float] = 546.468):
        await ctx.defer()
        if (ctx.guild is not None and ctx.guild.id not in whitelist) and ctx.author.id != bot.owner_id:
            await ctx.send("This server is not whitelisted for this command.")
            return

        def check_response(file_path, search_string):
            search_string = search_string.strip().lower()
            with open(file_path, 'r') as file:
                for line in file:
                    data = json.loads(line)
                    for message in data.get("messages", []):
                        if search_string == message.get("content", "").strip().lower():
                            return True
            return False

        file_path = f"{dannybot}\\assets\\pizzidata.jsonl"

        pizzi_text = ""
        while True:
            response = openai.ChatCompletion.create(
                model="ft:gpt-4o-mini-2024-07-18:personal:pizzi:9v9U1nDc:ckpt-step-1464",
                messages=[
                    {"role": "system", "content": "you are pizzi."},
                ],
                temperature=random.uniform(0.8, 1.35) if temperature == 546.468 else temperature,
                max_tokens=250,
                top_p=1.0,
                frequency_penalty=1.2,
                presence_penalty=1.6,
            )

            pizzi_text = response.choices[0].message.content[:2000]

            # check if the generated text matches any existing response in the JSONL file
            if not check_response(file_path, pizzi_text):
                break  # break the loop if the text is unique

        dooter_image = bag_random_dooter.choice('dooter')
        with open(f"{dannybot}\\database\\Dooter\\{dooter_image}", "rb") as f:
            await ctx.reply(pizzi_text, file=discord.File(f, "pizzi.png"))


    @commands.command(hidden=True)
    async def po(self, ctx):
        file_name = random.choice(os.listdir(f"{dannybot}\\database\\Po\\"))
        with open(f"{dannybot}\\database\\Po\\{file_name}", "rb") as f:
            await ctx.reply(file=File(f, "img.png"), mention_author=True)

    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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
            "leffrey",
            "femboy",
            "fanboy",
            "glasscup",
            "plasticcup",
            "burger",
            "danny",
        ] = "danny",
    ):
        await ctx.defer()
        if (ctx.guild is not None and ctx.guild.id not in whitelist) and ctx.author.id != bot.owner_id:
            await ctx.send("This server is not whitelisted for this command.")
            return

        if category not in self.bags:
            await ctx.reply(
                "Invalid category. Please choose from: " + ", ".join(self.bags.keys())
            )
            return
        
        bag = self.bags[category]
        try:
            file_name = bag.choice(category)
            file_path = os.path.join('database', category, file_name)
            with open(file_path, "rb") as f:
                await ctx.reply(file=File(f, "img.png"), mention_author=True)
        except ValueError:
            await ctx.reply("No files available in this category.")
        except FileNotFoundError:
            await ctx.reply("File not found.")

    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.hybrid_command(
        name="database",
        aliases=["db", "databases", "dbs"],
        description="Display file counts for key directories in Dannybot",
        brief="Display file counts for key directories in Dannybot",
    )
    async def db(self, ctx):
        if (ctx.guild is not None and ctx.guild.id not in whitelist) and ctx.author.id != bot.owner_id:
            await ctx.send("This server is not whitelisted for this command.")
            return
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
        }

        # Create the embed
        embed = discord.Embed(title="Dannybot File Totals", color=0xF77E9A)

        # Add fields to the embed
        for name, path in directory_paths.items():
            embed.add_field(
                name=name, value=f"{fileCount(path)} files\n{fileSize(path)}"
            )

        await ctx.reply(embed=embed, mention_author=True)

    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.hybrid_command()
    @commands.is_owner()
    async def kill(self, ctx, user: discord.User):
        count = 0
        on_cooldown = False
        async for message in ctx.channel.history(limit=None):
            if message.author != user:
                continue
            if (ctx.message.created_at - message.created_at).days < 14:
                try:
                    deleted = await ctx.channel.purge(
                        limit=100, check=lambda m: m.author == user, before=message
                    )
                    count += len(deleted)
                    break
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after)
                    else:
                        await ctx.send(f"Failed to bulk delete messages: {e}")
                        return
            if on_cooldown:
                await asyncio.sleep(1)
                on_cooldown = False
            try:
                await message.delete()
                count += 1
            except discord.NotFound:
                pass
            except discord.Forbidden:
                await ctx.send("I don't have permission to delete messages.")
                return
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after)
                    on_cooldown = True
                else:
                    await ctx.send(f"Failed to delete a message: {e}")
                    return

        await ctx.send(f"Deleted {count} messages from {user.mention}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(server(bot))

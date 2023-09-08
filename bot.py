# this is the file that boots up every other file.
# should really shouldnt need to touch this file ever

# if you can't find a variable used in this file its probably imported from here
from config import *

# make it look nice in the console
print("---------------------------------------------------------------------")
print("DANNYBOT IS STARTING UP... PLEASE WAIT...")
print("---------------------------------------------------------------------")

# asyncio bad btw
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# intents shit
intents = discord.Intents.all()
intents.voice_states = True
intents.messages = True

# We set up logger here
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define our prefix(es) and status
bot = commands.Bot(
    command_prefix=(dannybot_prefixes),
    status=discord.Status.online,
    activity=discord.Activity(name="d.help", type=1),
    intents=intents,
)


# do this when everything else is done
@bot.event
async def on_ready():
    print("---------------------------------------------------------------------")
    command_sync = await bot.tree.sync()
    print(f"Synced {len(command_sync)} slashes")
    # print a success message upon boot
    print("---------------------------------------------------------------------")
    print(f"{bot.user} successfully booted on discord.py version {discord.__version__}")
    print("---------------------------------------------------------------------")
    return


# this is our message handler
@bot.event
async def on_message(input):
    if input.author.bot:
        return
    is_denial = random.randint(0, dannybot_denialRatio) == dannybot_denialRatio and any(
        input.content.startswith(prefix) for prefix in dannybot_prefixes
    )

    if is_denial:
        await input.channel.send(
            random.choice(dannybot_denialResponses), reference=input
        )
    else:
        os.chdir(dannybot)  # Ensure we're in Dannybot's directory
        await bot.process_commands(input)


# this is a ping command and it's pretty self-explanatory
@bot.hybrid_command(
    name="ping",
    description="Calculate bot latency and send the results.",
    brief="Sends the current bot latency",
)
async def ping(ctx: commands.Context):
    ping_time = int(round(bot.latency * 1000))
    await ctx.send(content=f"Ping is {ping_time}ms")
    logger.info(f"Dannybot was pinged at {ping_time}ms")


# say command because every good bot should be a vessel for its creator to speak through - FDG
@bot.hybrid_command(
    name="say", description="DEV COMMAND | No description given", hidden=True
)
async def say(ctx: commands.Context, *, text):
    if not ctx.author.id in dannybot_team_ids:
        await ctx.reply("This command is restricted.", ephemeral=True, delete_after=3)
    else:
        await ctx.reply("say command issued.", ephemeral=True, delete_after=1)
        await ctx.channel.send(text)
        try:
            await ctx.message.delete()  # this only works for the text based
        except:
            return


@bot.hybrid_command(
    name="reload",
    description="DEV COMMAND | Reload specified cogs on the bot",
    hidden=True,
)
@commands.is_owner()
async def reload(ctx: commands.Context, module: str):
    if module == "all":
        cogs = [
            f"cogs.{filename[:-3]}"
            for filename in os.listdir("./cogs")
            if filename.endswith(".py")
        ]
    else:
        cogs = [f"cogs.{module}"]
    for cog in cogs:
        await bot.unload_extension(cog)
        await bot.load_extension(cog)
    await ctx.send(f"Reloaded {module} module(s)!")


# stage all of our cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            cog_path = f"cogs.{cog_name}"
            await bot.load_extension(cog_path)
            logger.info(f"Imported module: {cog_name}")


async def main():
    if clean_pooter_onLaunch:
        logger.info(
            "Cleaning up pooter folder... This may clog up the terminal if there are a lot of files..."
        )
        print("---------------------------------------------------------------------")
        clean_pooter()
        print("---------------------------------------------------------------------")
    if cache_clear_onLaunch:
        logger.info("Clearing cache from previous session...")
        print("---------------------------------------------------------------------")
        clear_cache()
        print("---------------------------------------------------------------------")

    await load_extensions()
    await bot.start(dannybot_token)


asyncio.run(main())

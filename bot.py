# this is the file that boots up every other file.
# should really shouldnt need to touch this file ever

# if you can't find a variable used in this file its probably imported from here
from config import *

# make it look nice in the console
print("---------------------------------------------------------------------")
print(Fore.LIGHTMAGENTA_EX + "DANNYBOT IS STARTING UP... PLEASE WAIT..." + Fore.RESET)
print("---------------------------------------------------------------------")

# stupid shit
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
intents = discord.Intents.all()
AppCommandContext.guild = True

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import prefixes
dannybot_prefixes = dannybot_prefixes

# initialize the bot
bot = commands.AutoShardedBot(
    command_prefix=dannybot_prefixes,
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=discord.ActivityType.watching),
    intents=intents,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print("---------------------------------------------------------------------")
    command_sync = await bot.tree.sync()
    print(Fore.BLUE + f"Synced {len(command_sync)} slashes" + Fore.RESET)
    print("---------------------------------------------------------------------")
    print(
        Fore.GREEN
        + f"{bot.user} successfully booted on discord.py version {discord.__version__} with {bot.shard_count} shards"
        + Fore.RESET
    )
    print("---------------------------------------------------------------------")
    return


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    has_prefix = any(message.content.startswith(prefix) for prefix in dannybot_prefixes)
    is_denial = (
        random.randint(0, dannybot_denialRatio) == dannybot_denialRatio
    ) and has_prefix

    if is_denial:
        await message.channel.send(
            random.choice(dannybot_denialResponses), reference=message
        )
    elif has_prefix:
        os.chdir(dannybot)  # idk why it does this but let's not find out why
        await bot.process_commands(message)


@bot.hybrid_command(
    name="ping",
    description="Calculate bot latency and send the results.",
    brief="Sends the current bot latency",
)
async def ping(ctx: commands.Context):
    start_time = time.monotonic()
    message = await ctx.send("Round-trip Latency: NANms | API Latency: NANms")
    end_time = time.monotonic()
    ping_time = round((end_time - start_time) * 1000)
    await message.edit(
        content=f"Round-trip Latency: {ping_time}ms | API Latency: {round(bot.latency * 1000)}ms"
    )


@bot.hybrid_command(
    name="say", description="DEV COMMAND | No description given", hidden=True
)
async def say(ctx: commands.Context, *, text):
    if ctx.author.id not in dannybot_team_ids:
        await ctx.reply("This command is restricted.", ephemeral=True, delete_after=3)
    else:
        await ctx.reply("say command issued.", ephemeral=True, delete_after=1)
        await ctx.channel.send(text)
        try:
            await ctx.message.delete()  # this only works for text-based messages
        except Exception:
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

    # loop through each specified cog to unload and reload
    for cog in cogs:
        try:
            await bot.unload_extension(cog)
        except discord.ext.commands.errors.ExtensionNotLoaded:
            pass
        await bot.load_extension(cog)

    # eesynchronize slash commands
    command_sync = await bot.tree.sync()
    print(Fore.BLUE + f"Synced {len(command_sync)} slashes" + Fore.RESET)
    await ctx.send(f"Reloaded {module} module(s)!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.invoked_with.startswith(
        "poo"
    ):
        return
    raise error


async def load_extension(cog):
    try:
        await bot.load_extension(cog)
        print(
            Fore.LIGHTMAGENTA_EX
            + "Imported module: "
            + Fore.LIGHTCYAN_EX
            + f"{cog}"
            + Fore.RESET
        )
    except Exception as e:
        print(Fore.RED + f"Failed to load {cog}: {e}" + Fore.RESET)


async def load_extensions():
    tasks = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            cog_path = f"cogs.{cog_name}"
            tasks.append(asyncio.create_task(load_extension(cog_path)))
    await asyncio.gather(*tasks)


# this ACTUALLY starts the bot
async def main():
    if clean_pooter_onLaunch:
        print(
            Fore.LIGHTMAGENTA_EX
            + "Cleaning up pooter folder... This may clog up the terminal if there are a lot of files..."
            + Fore.RESET
        )
        print("---------------------------------------------------------------------")
        clean_pooter()
        print("---------------------------------------------------------------------")
    if cache_clear_onLaunch:
        print(
            Fore.LIGHTMAGENTA_EX
            + "Clearing cache from the previous session..."
            + Fore.RESET
        )
        print("---------------------------------------------------------------------")
        clear_cache()
        print("---------------------------------------------------------------------")
    await load_extensions()
    await bot.start(dannybot_token)


asyncio.run(main())

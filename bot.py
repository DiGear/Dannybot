# this is the file that boots up every other file.
# should really shouldnt need to touch this file ever

# if you can't find a variable used in this file its probably imported from here
from config import *

# make it look nice in the console
print("-----------------------------------------")
print("DANNYBOT IS STARTING UP... PLEASE WAIT...")
print("-----------------------------------------")

# asyncio bad btw
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# intents shit
intents=discord.Intents.all()
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
    # name corrector
    for guild in bot.guilds:
        try:
            await guild.me.edit(nick=bot.user.name)
            logger.info(f'Corrected name in {guild.name}')
        except discord.Forbidden:
            logger.error(f'Unable to correct name in {guild.name}')
    # print a success message upon boot
    print("---------------------------------------------------------------------")
    print(f"{bot.user} successfully booted on discord.py version {discord.__version__}")
    print("---------------------------------------------------------------------")
    return

# this is our message handler
@bot.event
async def on_message(input):
    is_denial = (
        random.randint(0, dannybot_denialRatio) == dannybot_denialRatio
        and any(input.content.startswith(prefix) for prefix in dannybot_prefixes)
    )

    if is_denial:
        await input.channel.send(random.choice(dannybot_denialResponses), reference=input)
    else:
        os.chdir(dannybot)  # Ensure we're in Dannybot's directory
        await bot.process_commands(input)

# this is a ping command and it's pretty self-explanatory
@bot.command(description="Calculate bot latency using time.monotonic(), and send the results.", brief="Sends the current bot latency")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Ping is...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Ping is {int(ping)}ms")
    logger.info(f'Dannybot was pinged at {int(ping)}ms')

# say command because every good bot should be a vessel for its creator to speak through - FDG
@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, args):
    args = args.replace('@', '@\u200b')  # Prevent accidental mentions

    for guild in bot.guilds:
        for member_id in args.split():
            if member_id.isdigit():
                member = get(guild.members, id=int(member_id))
                if member:
                    args = args.replace(member_id, member.mention)
    await ctx.send(args)
    await ctx.message.delete()

# theres definitely a better way to do this
@bot.command(description="Delete the most recent command output in the current channel. This only affects Dannybot.", brief="Undo the last command output")
async def undo(ctx):
    async for msg in ctx.channel.history(limit=500):
        if msg.author.id == bot.user.id:
            await msg.delete()
            return

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, module):
    if module == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cog_name = filename[:-3]
                cog_path = f"cogs.{cog_name}"
                await bot.unload_extension(cog_path)
                await bot.load_extension(cog_path)
        await ctx.send("Reloaded all modules!")
    else:
        cog_path = f"cogs.{module}"
        await bot.unload_extension(cog_path)
        await bot.load_extension(cog_path)
        await ctx.send(f"Reloaded {module} module!")
        
@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, module):
    if module == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cog_name = filename[:-3]
                cog_path = f"cogs.{cog_name}"
                await bot.unload_extension(cog_path)
        await ctx.send("Unloaded all modules!")
    else:
        cog_path = f"cogs.{module}"
        await bot.unload_extension(cog_path)
        await ctx.send(f"Unloaded {module} module!")

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, module):
    if module == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cog_name = filename[:-3]
                cog_path = f"cogs.{cog_name}"
                await bot.load_extension(cog_path)
        await ctx.send("Loaded all modules!")
    else:
        cog_path = f"cogs.{module}"
        await bot.load_extension(cog_path)
        await ctx.send(f"Loaded {module} module!")

# stage all of our cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            cog_path = f"cogs.{cog_name}"
            await bot.load_extension(cog_path)
            logger.info(f"Imported module: {cog_name}")

async def main():
    if cache_clear_onLaunch:
        logger.info("Clearing cache from previous session...")
        clear_cache()

    await load_extensions()
    await bot.start(dannybot_token)

asyncio.run(main())
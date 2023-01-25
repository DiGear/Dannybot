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

if cache_clear_onLaunch:
    print("clearing cache from previous session...")
    clear_cache()
    print("-----------------------------------------")

bot = commands.Bot(
    command_prefix=(dannybot_prefix),
    status=discord.Status.online,
    activity=discord.Activity(name="for d.help", type=3),
    intents=discord.Intents.all(),
)

# print a success message upon boot, and then change the bots activity
@bot.event
async def on_ready():
    print("---------------------------------------------------------------------")
    print(f"{bot.user} successfully booted on discord.py version {discord.__version__}")
    print("---------------------------------------------------------------------")
    await bot.change_presence(activity=discord.Activity(type=discord.Activity(name="for d.help", type=3)))
    return

# check if config.debug_mode is true and treat the message handler appropriately
@bot.event
async def on_message(input):
    if (debug_mode and input.content.startswith(bot.command_prefix) and input.author.id not in devs):
        await input.channel.send("Developer mode is active. Only verified developers can interact with the bot at this time.")
    else:
        await bot.process_commands(input)

# error handling code
# theres probably a better way to do this - FDG
@bot.event
async def on_command_error(ctx, error):
    # ignore "intentional errors"/errors that get caught mid-function
    if hasattr(ctx.command, "on_error"):
        return

    # ignore errors that happen in cogs that contain error handlers already
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    # set specific errors to be ignored, such as the commands.CommandNotFound error
    ignored = (commands.CommandNotFound,)

    error = getattr(error, "original", error)

    # ignore errors in the ignore list
    if isinstance(error, ignored):
        return

    # command is disabled
    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f"{ctx.command} has been disabled.")

    # command requires developer permissions
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.send(f"{ctx.command} is reserved for Dannybot developers.")

    # command was sent in a DM
    elif isinstance(error, commands.NoPrivateMessage):
        # send the error response in the DM, if possible
        try:
            await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
        except discord.HTTPException:
            pass
    else:
        # this is a catch-all for any other types of errors, they will be sent in chat and the console for debugging purposes
        await ctx.send(
            "An undefined error has occured.\n```\n"
            + str(error.__traceback__)
            + "\n"
            + str(error)
            + "```\nIf you are seeing this, ping FDG for assistance."
        )
        print("Ignoring exception in command {}:".format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

# this is a ping command and it's pretty self-explanatory
@bot.command(description="Calculate bot latency using time.monotonic(), and send the results.", brief="Sends the current bot latency")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Ping is...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Ping is {int(ping)}ms")
    print(f'Dannybot was pinged at {int(ping)}ms')

# say command because every good bot should be a vessel for its creator to speak through - FDG
@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, args):
    await ctx.send(args)
    # delete the command message, leaving only what Dannybot sends
    await ctx.message.delete()

@bot.command(hidden=True)
@commands.is_owner()
async def dbpurge(ctx):
    invalidFiles = 0
    for file in os.listdir(f'{dannybot}\\database\\Pooter'):
        ext = file.split('.')[-1].lower()
        if ext not in database_acceptedFiles:
            os.remove(f'{dannybot}\\database\\Pooter\\{file}')
            invalidFiles =+ 1
    await ctx.send(f'Purged Pooter database of {invalidFiles} invalid files!')

@bot.command(description="Delete the most recent command output in the current channel. This only affects Dannybot.", brief="Undo the last command output")
async def undo(ctx):
    channel = ctx.message.channel
    async for msg in channel.history(limit=500):
        if msg.author.id == 847276836172988426:
            await msg.delete()
            return

# this command reloads a specified cog. used for testing, you can call this command to update code on a cog without restarting the whole bot
@bot.command(description="This is an owner only command. It allows for any module to be reloaded on the fly.", brief="Debug tool for modules")
@commands.is_owner()
async def reload(ctx, module):
    await bot.unload_extension(f"cogs.{module}")
    await bot.load_extension(f"cogs.{module}")
    await ctx.send(f"Reloaded {module} module!")

@bot.command(description="This is an owner only command. It clears Dannybots cache of all temporary files.", brief="Clears Dannybots cache")
@commands.is_owner()
async def cache(ctx):
    for file in os.listdir(f'{dannybot}\\cache'):
        if 'git' not in file and '.' in file:
            os.remove(f'{dannybot}\\cache\\{file}')
    await ctx.send(f"Cleared cache!")

# stage all of our cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print("imported module: " + f"{filename[:-3]}")

# load all of our cogs and start the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(dannybot_token)

asyncio.run(main())
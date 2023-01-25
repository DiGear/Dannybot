# theres probably a better way to do this - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *


class errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        # ignore "intentional errors": errors that get caught mid-function
        if hasattr(ctx.command, "on_error"):
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
            await ctx.send(f"{ctx.command} is reserved for Dannybot developers. <:trollface:855665633509507092>") # trollface emote is from dannybots mother server, will need to replace emote or remove it

        # command was sent in a DM
        elif isinstance(error, commands.NoPrivateMessage):
            try: # send the error response in the DM, if possible
                await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
            except discord.HTTPException:
                pass
        else:
            # this is a catch-all for any other types of errors, they will be sent in chat and the console for debugging purposes
            await ctx.send(f"An undefined error has occured.\n```\n{error.__traceback__}\n{error}```\nIf you are seeing this, ping FDG for assistance.")
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot: commands.Bot):
    await bot.add_cog(errors(bot))

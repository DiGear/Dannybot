# theres probably a better way to do this - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *


class errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore "intentional errors": errors that get caught mid-function
        if hasattr(ctx.command, "on_error"):
            return

        # Set specific errors to be ignored, such as commands.CommandNotFound
        ignored = (commands.CommandNotFound,)

        error = getattr(error, "original", error)

        # Ignore errors in the ignore list
        if isinstance(error, ignored):
            return

        # Command is disabled
        if isinstance(error, commands.DisabledCommand):
            await ctx.reply(f"{ctx.command} has been disabled.")

        # Command requires developer permissions
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.reply(f"{ctx.command} is reserved for Dannybot developers. <:trollface:855665633509507092>")  # Replace or remove the trollface emote

        # Command was sent in a DM
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
            except discord.HTTPException:
                pass

        else:
            # Handle other types of errors
            error_message = f"An undefined error has occurred.\n```py\n{type(error).__name__}: {error}\n```"
            await ctx.reply(error_message)
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(bot: commands.Bot):
    await bot.add_cog(errors(bot))

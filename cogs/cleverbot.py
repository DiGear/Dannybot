# this cog only exists to manage the cleverbot api
# it just looked really bad to run all of this in the main files on_message function

# if you can't find a variable used in this file its probably imported from here
from data import *

load_dotenv()
cw = CleverWrap(os.getenv("CLEVERBOT_KEY"))


class cleverbot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        # check for a valid "talk to dannybot" channel
        if "talk-to-dannybot" in str(input.channel.name):
            # make sure the user isn't a bot
            if not input.author.bot:
                # this resets the conversation upon request
                if "new conversation" in input.content:
                    cw.reset()
                    return
                elif "> " in input.content:
                    return
                else:
                    # send the resulting message cleverbot api returns for our given unput
                    await input.channel.send(cw.say(input.content), reference=input)
                    return


async def setup(bot: commands.Bot):
    await bot.add_cog(cleverbot(bot))

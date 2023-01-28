# this cog only exists to manage the cleverbot api
# it just looked really bad to run all of this in the main files on_message function - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Cleverbot.reset()
        print('Cleverbot memory wiped!')

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        rng = None
        
        rng = random.randint(0, dannybot_sentienceRatio)
        if "." in input.content:
            return
       
        if rng == dannybot_sentienceRatio and not input.author.bot and not input.content.startswith(dannybot_prefix) or "dannybot" in input.content:
        
            # declare the response as a variable
            response = Cleverbot.say(input.content)
            
            # remove all punctuation and capitalization to make it seem more discord user-like
            response = str(response.translate(str.maketrans('', '', string.punctuation))).lower()
            
            reponse = response.replace('dannybot', '')
            
            # send the resulting message cleverbot api returns for our given unput
            await input.channel.send(response)
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))

# this cog only exists to manage the cleverbot api
# it just looked really bad to run all of this in the main files on_message function - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

nameRecall_list = ['buddy', 'pal', 'dude', 'bro']

class cleverbot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        # check for a valid "talk to dannybot" channel and make sure the user isn't a bot
        if "talk-to-dannybot" in str(input.channel.name) and not input.author.bot:
            
            # this resets the conversation upon request
            if "new conversation" in input.content:
                Cleverbot.reset()
                return
            elif "> " in input.content:
                return
            else:
                
                # declare the response as a variable
                response = Cleverbot.say(input.content)
                
                # remove all punctuation and capitalization to make it seem more discord user-like
                response = str(response.translate(str.maketrans('', '', string.punctuation))).lower()
                
                # dumb - FDG
                for i in range(len(nameRecall_list)):
                    response = response.replace(nameRecall_list[i], str(input.author.name))
                
                # send the resulting message cleverbot api returns for our given unput
                await input.channel.send(response, reference=input)
                return


async def setup(bot: commands.Bot):
    await bot.add_cog(cleverbot(bot))

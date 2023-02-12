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

            response = str(response.translate(str.maketrans('', '', string.punctuation))).upper()
            
            reponse = response.replace('dannybot', '')
            
            rng = random.randint(0,4)
            
            # send the resulting message cleverbot api returns for our given unput
            if rng == 4:
                pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
                with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                    await input.channel.send(response, reference=input, file=discord.File(pooter_file))
            else:
                await input.channel.send(response, reference=input)  
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))

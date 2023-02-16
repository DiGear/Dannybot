# this cog only exists to manage the cleverbot api
# it just looked really bad to run all of this in the main files on_message function - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        rng = None
        
        rng = random.randint(0, dannybot_sentienceRatio)
        if "." in input.content:
            return
       
        if input.author.bot:
           return
       
        if rng == dannybot_sentienceRatio and not input.author.bot and not input.content.startswith(dannybot_prefix) or "dannybot" in input.content:
        
            # declare the response as a variable
            parsedInput = input.content.replace("dannybot", "")
            gpt_prompt = str(f"have a conversation with me\nme: {parsedInput}")
            
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )

            response = response.split(":")
            
            # send the resulting message cleverbot api returns for our given unput
            await input.channel.send(response[1], reference=input)
            
            # random image chance
            rng = random.randint(0,4)
            if rng == 4:
                pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
                with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                    picture = discord.File(f)
                    await input.channel.send(file=picture, filename="dannybot")
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))

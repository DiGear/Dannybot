# this cog only exists to manage the GPT3 api
# it just looked really bad to run all of this in the main files on_message function - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        rng = random.randint(0, dannybot_sentienceRatio) # random number generator
        if "." in input.content and not "dannybot" in input.content:
            return
        if input.author.bot: # if the author is a bot
            return
        if rng == dannybot_sentienceRatio and not input.author.bot and not input.content.startswith(dannybot_prefix) or "dannybot" in input.content:
        
            # declare the response as a variable and set it to the openai api
            gpt_prompt = str(f"Respond to the following chat message. {input.author.name}: {input.content} Dannybot::")
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
            response = response['choices'][0]['text']
            
            # send the resulting message openai api returns for our given input
            await input.channel.send(response, reference=input)
            
            # random image chance, send a random image from the pooter folder
            rng = random.randint(0,4)
            if rng == 4:
                pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
                with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                    picture = discord.File(f)
                    await input.channel.send(file=picture, filename="dannybot")
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
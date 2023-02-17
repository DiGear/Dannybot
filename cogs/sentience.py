# this cog only exists to manage the GPT3 api
# it just looked really bad to run all of this in the main files on_message function - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        
        # im waiting for ChatGPT access to do this, I just wanted to get a headstart on the code - FDG
        self.conversing = False
        self.conversing_user = None
        self.conversing_channel = None
        
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        rng = random.randint(0, dannybot_sentienceRatio)
        if "." in input.content and not "dannybot" in input.content and not self.conversing and not input.content.startswith(dannybot_prefix): # if the message contains a period and is not a command or a message to dannybot
            return
        if input.author.bot: # if the author is a bot
            return
        if rng == dannybot_sentienceRatio and not input.author.bot and not input.content.startswith(dannybot_prefix) or "dannybot" in input.content or self.conversing: # if the random number generator is equal to the sentience ratio and the message is not a command or a message to dannybot
        
            # declare the response as a variable and set it to the openai api
            if self.conversing: # if the bot is conversing with someone
                gpt_prompt = str(f"Respond to the following chat message. {self.conversing_user}: {input.content} Dannybot::")
            else: # if the bot is not conversing with someone
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
            if self.conversing: # if the bot is conversing with someone
                await self.conversing_channel.send(response, reference=input)
            else: # if the bot is not conversing with someone
                await input.channel.send(response, reference=input)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
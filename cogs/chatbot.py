# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        
        # im waiting for ChatGPT access to do this, I just wanted to get a headstart on the code - FDG
        self.conversing = False
        self.conversing_user = None
        self.conversing_channel = None
       
# my plan is to have this toggled by start and stop emotes that dannybot appends to every messages he sends
# you can click the start emote once to begin conversing and click to stop button to end conversing

        # self.conversing = True
        # self.conversing_user = input.author.name
        # self.conversing_channel = input.channel
        
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        if "." in input.content and not "dannybot" in input.content.lower() and not self.conversing and not any(input.content.startswith(prefix) for prefix in dannybot_prefixes): # if the message contains a period and is not a command or a message to dannybot or the bot is conversing with someone
            return
        if input.author.bot: # if the author is a bot or the bot is conversing with someone
            return
        if not input.author.bot and input.content.lower().startswith("dannybot") or input.content.lower().endswith("dannybot") or self.conversing: # if the random number generator is equal to the sentience ratio and the message is not a command or a message to dannybot or the bot is conversing with someone
        
            # declare the response as a variable and set it to the openai api
            if self.conversing: # if the bot is conversing with someone
                gpt_prompt = str(f"Respond to the following chat message. {self.conversing_user}: {input.content} Dannybot::")
            else: # if the bot is not conversing with someone
                gpt_prompt = str(f"Respond to the following chat message. {input.author.name}: {input.content} Dannybot::")
            response = openai.Completion.create( # get the response from the openai api
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
            
            # send the resulting message openai api returns for our given input
            if self.conversing: # if the bot is conversing with someone
                await self.conversing_channel.send(response['choices'][0]['text'], reference=input)
            else: # if the bot is not conversing with someone
                await input.channel.send(response['choices'][0]['text'], reference=input)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
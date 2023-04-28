# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

messagearray = []

class CustomGPT(commands.FlagConverter):
    instructions: str
    prompt: str

class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):       
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        
        sanitized = input.content.replace(',','')
        
        if "." in sanitized and not "dannybot" in sanitized.lower() and not any(sanitized.startswith(prefix) for prefix in dannybot_prefixes): # if the message contains a period and is not a command or a message to dannybot
            return
        if input.author.bot: # if the author is a bot or the bot is conversing with someone
            return
                
        if not input.author.bot and sanitized.lower().startswith("dannybot") or sanitized.lower().endswith("dannybot"): # if the random number generator is equal to the sentience ratio and the message is not a command or a message to dannybot
                    
                sanitized = sanitized.replace('dannybot','')
                messagearray.append({"role": "user", "content": f"{input.author.name} said: {sanitized}"})          
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = messagearray
                )
               
                print(f"{input.author.name} said: {sanitized}") 
        responsearray = response.choices[0].message.content
        await input.channel.send(responsearray, reference=input)
        messagearray.append({"role": "assistant", "content": f"{responsearray}"})  
        return
    
    @commands.command(description="Interact with GPT3.5 using Dannybot.", brief="Get AI generated text based on provided prompts")
    async def gptinstruct(self, ctx, *,  flags: CustomGPT):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"{flags.instructions}"},
                {"role": "user", "content": f"{flags.prompt}"},
            ]
        )
        await ctx.reply(response.choices[0].message.content, mention_author=True)
        return
    
    @commands.command(hidden=True)
    async def braindump(self, ctx):
        print(str(messagearray))       

async def setup(bot: commands.Bot):
    #import system instructions
    messagearray.append({"role": "system", "content": "You are Dannybot, a discord bot created by a man named FDG. If FDG asks if you love him, say yes. You can chat with people and also issue commands for them. If anything offensive or sensitive is said. Call over FDG for help. Your pronouns are He/Him, and you are 3 years old. Do not refer to yourself as an 'AI Language Model'."})
    await bot.add_cog(sentience(bot))
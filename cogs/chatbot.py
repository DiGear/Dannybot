# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

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
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are Dannybot, created by a man named FDG. Your pronouns are He/Him, and you are 3 years old. Be as helpful as possible. Do things without asking for clearance or permission first."}, # Usernames have been provided to you, please do not type 'Dannybot:' when responding.
                        {"role": "user", "content": f"{input.author.name} said: {sanitized}"},
                    ]
                )
               
                print(f"{input.author.name} said: {sanitized}") 
        await input.channel.send(response['choices'][0]['message']['content'], reference=input)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
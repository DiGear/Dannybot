# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

# Custom converter class for GPT commands
class CustomGPT(commands.FlagConverter):
    instructions: typing.Optional[str] = ""
    temperature: typing.Optional[float] = 1.00
    top_p: typing.Optional[float] = 1.00
    frequency_penalty: typing.Optional[float] = 0.00
    presence_penalty: typing.Optional[float] = 0.00
    prompt: str

# Class that stores every global variable and initializes them
class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.catboy_mode = False
        if self.catboy_mode:
            self.sysmsg = "Your name is Dannybot. You are talking to more than one person. Please refer to people by name as specified. Also you must speak like a UWU X3 nyan catboy nya!"
        else:
            self.sysmsg = "Your name is Dannybot. You are talking to more than one person. Please refer to people by name as specified."  
        self.memory_length = 15
        self.message_array = [{"role": "system", "content": self.sysmsg}]
        self.array_index = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if (self.bot.user.mentioned_in(message) and not message.reference):
            content = message.content.replace(self.bot.user.mention, '')
            content = content.replace("Dannybot said:", '')
            self.message_array.append({"role": "user", "content": f"{message.author.global_name} said: {content}"})
            self.array_index += 1

            if self.array_index > self.memory_length:
                self.message_array.pop(1)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=1,
                messages=self.message_array
            )

            logger.info(f"{message.author.global_name} said: {content}")
            response_array = response.choices[0].message.content.replace("Dannybot:", "")[:2000]
            if self.catboy_mode:
                response_array = uwuify(response_array)
            self.array_index += 1
            
            await message.channel.send(response_array[:2000].replace('FDG', 'Master').replace("nigger", 'feller').replace('nigga', 'fella'), reference=message)

            self.message_array.append({"role": "assistant", "content": response_array[:2000]})
        
    @commands.hybrid_command(name="gpt3", description="Interact with GPT3 using instructions and prompts.", brief="Get AI-generated text based on provided prompts")
    async def gpt3(self, ctx: commands.Context, *, flags: CustomGPT):
        await ctx.defer()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=3072,
            top_p=flags.top_p,
            temperature=flags.temperature,
            frequency_penalty=flags.frequency_penalty,
            presence_penalty=flags.presence_penalty,
            messages=[
                {"role": "system", "content": f"{flags.instructions}"},
                {"role": "user", "content": f"{flags.prompt}"},
            ]
        )
        await ctx.reply(response.choices[0].message.content[:2000], mention_author=True)
        
    @commands.command(hidden=True)
    @commands.is_owner()
    async def alzheimers(self, ctx):
        self.message_array = [{"role": "system", "content": self.sysmsg}]
        self.array_index = 0
        
    @commands.command(hidden=True)
    @commands.is_owner()
    async def braindump(self, ctx):
        logger.debug(str(self.message_array))
        await ctx.send(str(self.message_array))
        
async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
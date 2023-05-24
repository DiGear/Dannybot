# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

# Custom converter class for GPT commands
class CustomGPT(commands.FlagConverter):
    instructions: str
    prompt: str

# Class that stores every global variable and initializes them
class charai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.memory_length = 15
        self.message_array = []
        self.array_index = 0
        self.allowed_in_voice_channel = False
        self.token = characterAI_key

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message) and not message.reference:
            content = message.content.replace(self.bot.user.mention, '')
            self.message_array.append({"role": "user", "content": f"{message.author.name} said: {content}"})
            self.array_index += 1

            if self.array_index > self.memory_length:
                self.message_array.pop(1)

            client = pyCAI(self.token)
            data = client.chat.send_message('CHAR', content, wait=True)
            response_array = data['replies'][0]['text']

            logger.info(f"{message.author.name} said: {content}")

            await message.channel.send(response_array, reference=message)

            self.message_array.append({"role": "assistant", "content": response_array})

    @commands.command(description="Interact with GPT3.5 using Dannybot.", brief="Get AI-generated text based on provided prompts")
    async def gptinstruct(self, ctx, *, flags: CustomGPT):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{flags.instructions}"},
                {"role": "user", "content": f"{flags.prompt}"},
            ]
        )
        await ctx.reply(response.choices[0].message.content, mention_author=True)
        
    @commands.command(hidden=True)
    @commands.is_owner()
    async def alzheimers(self, ctx):
        self.array_index = 0
        
async def setup(bot: commands.Bot):
    await bot.add_cog(charai(bot))
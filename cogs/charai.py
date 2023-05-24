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
        self.sysmsg = "pretend you are a sassy black woman"
        self.memory_length = 15
        self.message_array = [{"role": "system", "content": self.sysmsg}]
        self.array_index = 0
        self.allowed_in_voice_channel = False

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

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=1,
                messages=self.message_array
            )

            logger.info(f"{message.author.name} said: {content}")
            response_array = response.choices[0].message.content.replace("Dannybot:", "")
            self.array_index += 1

            if message.author.voice and message.author.voice.channel:
                voice_state = message.guild.voice_client
                voice_channel = message.author.voice.channel

                if voice_state and voice_state.is_playing():
                    pass
                else:
                    if self.allowed_in_voice_channel:
                        voice_client = voice_state or await voice_channel.connect()

                engine = pyttsx3.init()
                engine.setProperty('rate', random.randint(125, 175))
                engine.setProperty('volume', 0.75)
                output_file = f"{dannybot}\\cache\\ChatGPT.wav"
                text = response_array
                engine.save_to_file(text, output_file)
                engine.runAndWait()

                await message.channel.send(response_array, reference=message)
                if self.allowed_in_voice_channel:
                    audio_source = discord.FFmpegPCMAudio(f"{dannybot}\\cache\\ChatGPT.wav")
                    voice_client.play(audio_source)
            else:
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
        self.message_array = [{"role": "system", "content": self.sysmsg}]
        self.array_index = 0
        
    @commands.command(hidden=True)
    @commands.is_owner()
    async def braindump(self, ctx):
        logger.debug(str(self.message_array))
        await ctx.send(str(self.message_array))
        
async def setup(bot: commands.Bot):
    await bot.add_cog(charai(bot))
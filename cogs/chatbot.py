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
    model: Literal[
        "gpt-4o",
        "gpt-4-turbo-preview",
        "gpt-4",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo"
    ]

# Custom converter class for Voice commands
class CustomVoice(commands.FlagConverter):
    whisper_api_key: str = str(os.getenv("OPENAI_API_KEY"))

# TranscriptionSink class for handling audio transcription
class TranscriptionSink(AudioSink):
    def __init__(self, whisper_api_key, bot, ctx):
        super().__init__()
        self.whisper_api_key = whisper_api_key 
        self.bot = bot
        self.ctx = ctx
    
    def wants_opus(self):
        return False  # Or True, depending on your requirements

    def write(self, user, data):
        # Ensure the data is in the correct format
        if isinstance(data, discord.VoiceData):
            # Extract audio data from the VoiceData object
            audio_data = data.data
            # Perform speech recognition using Whisper API
            with tempfile.NamedTemporaryFile(suffix='.opus') as temp_file:
                temp_file.write(audio_data)
                temp_file.seek(0)
                # Initialize Whisper client with API key
                whisper_client = Whisper(api_key=self.whisper_api_key)
                transcription = whisper_client.transcribe_audio(temp_file.name)

            # Pass the transcription to the ChatGPT model and get the response
            model = "gpt-4o"
            response_data = openai.ChatCompletion.create(
                model=model,
                temperature=1,
                messages=[{"role": "user", "content": transcription.text}],
            )

            response_text = response_data.choices[0].message.content
            response_text = re.sub(r'(?i)dannybot:', '', response_text)
            response_text = re.sub(r'(?i)dannybot said:', '', response_text).strip()[:1990]

            # Speak the response in the voice channel
            voice_channel = self.ctx.author.voice.channel
            if voice_channel:
                voice_client = discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild)
                if voice_client:
                    voice_client.play(discord.FFmpegPCMAudio(response_text, pipe=True))
                else:
                    asyncio.run_coroutine_threadsafe(voice_channel.connect(), self.bot.loop)

    def cleanup(self):
        pass

# chatbot class for handling ChatGPT commands
class Chatbot(commands.Cog):
    def __init__(self, bot: commands.Bot, memory_length=12):
        self.bot = bot
        self.memory_length = memory_length
        self.message_array = deque([{"role": "system", "content": '''
            Your name is Dannybot. You are talking to more than one person. Please refer to people by name as specified (The name will be display as "name said:").
            '''}], maxlen=memory_length + 1)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.reference:
            return

        if message.guild.id not in whitelist:
            return

        if self.bot.user.mentioned_in(message):
            content = [{"type": "text", "text": f"{message.author.display_name} said: {message.content}"}]

            if message.attachments:
                attachment_url = message.attachments[0].url
                content.append({"type": "image_url", "image_url": {"url": str(attachment_url)}})

            self.message_array.append({"role": "user", "content": content})

            if len(self.message_array) > self.memory_length:
                self.pop_not_sys()

            model = "gpt-4o"
            response_data = openai.ChatCompletion.create(
                model=model,
                temperature=1,
                messages=list(self.message_array)
            )

            response_text = response_data.choices[0].message.content
            response_text = re.sub(r'(?i)dannybot:', '', response_text)
            response_text = re.sub(r'(?i)dannybot said:', '', response_text).strip()[:1990]

            await message.channel.send(response_text, reference=message)
            self.message_array.append({"role": "assistant", "content": response_text})

    def pop_not_sys(self):
        for msg in reversed(self.message_array):
            if msg["role"] != "system":
                self.message_array.remove(msg)
                break

    @commands.hybrid_command(
        name="chatgpt",
        description="Interact with ChatGPT using instructions and prompts.",
        brief="Get AI-generated text based on provided prompts",
    )
    async def chatgpt(self, ctx: commands.Context, *, flags: CustomGPT):
        await ctx.defer()
        if ctx.guild.id not in whitelist:
            await ctx.send("This server is not whitelisted for this command.")
            return
        response = openai.ChatCompletion.create(
            model=flags.model,
            max_tokens=512,
            top_p=flags.top_p,
            temperature=flags.temperature,
            frequency_penalty=flags.frequency_penalty,
            presence_penalty=flags.presence_penalty,
            messages=[
                {"role": "system", "content": f"{flags.instructions}"},
                {"role": "user", "content": f"{flags.prompt}"},
            ],
        )
        await ctx.reply(response.choices[0].message.content[:2000], mention_author=True)

    @commands.command()
    async def start_voice_transcription(self, ctx: commands.Context, *, flags: CustomVoice):
        # Get the voice channel the author of the command is currently connected to
        voice_channel = ctx.author.voice.channel

        if voice_channel:
            # Connect to the voice channel using VoiceRecvClient
            voice_client = await voice_channel.connect(cls=VoiceRecvClient)

            # Start listening to the voice channel and pass the transcription sink
            voice_client.listen(TranscriptionSink(flags.whisper_api_key, self.bot, ctx))

            await ctx.send("Started voice transcription.")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def stop_voice_transcription(self, ctx: commands.Context):
        # Disconnect from the voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Stopped voice transcription.")
        else:
            await ctx.send("Not currently connected to a voice channel.")

# Function to setup the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(Chatbot(bot))
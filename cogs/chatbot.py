# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

# Custom converter class for GPT commands
class CustomGPT(commands.FlagConverter):
    instructions: str
    prompt: str

# Class that stores every global variable and initializes them
class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot):       
        self.bot = bot
        self.sysmsg = "You are Dannybot, a discord bot created by a man named FDG. You can chat with people and also issue commands for them. Your pronouns are He/Him, and you are 3 years old. Do not refer to yourself as an 'AI Language Model'."
        self.arrayindex = 0
        self.memorylength = 15
        self.messagearray = []
        self.messagearray.append({"role": "system", "content": f"{self.sysmsg}"})
        self.allowedInVC = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.replace(',', '')
        is_command = any(content.startswith(prefix) for prefix in dannybot_prefixes)

        if "." in content and not "dannybot" in content.lower() and not is_command:
            return

        if not message.author.bot and ("dannybot" in content.lower() or content.lower().endswith("dannybot")):
            content = content.replace('dannybot', '')

            self.messagearray.append({"role": "user", "content": f"{message.author.name} said: {content}"})
            self.arrayindex += 1

            if self.arrayindex > self.memorylength:
                self.arrayindex = 0
                self.messagearray = []
                self.messagearray.append({"role": "system", "content": f"{self.sysmsg}"})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messagearray
            )

            print(f"{message.author.name} said: {content}")
            responsearray = response.choices[0].message.content
            self.arrayindex += 1

            if message.author.voice and message.author.voice.channel:
                voice_state = message.guild.voice_client
                voice_channel = message.author.voice.channel

                if voice_state and voice_state.is_playing():
                    pass
                else:
                    if self.allowedInVC:
                        voice_client = voice_state or await voice_channel.connect()

                engine = pyttsx3.init()
                engine.setProperty('rate', random.randint(125, 175))
                engine.setProperty('volume', 0.75)
                output_file = 'ChatGPT.wav'
                text = responsearray
                engine.save_to_file(text, output_file)
                engine.runAndWait()

                await message.channel.send(responsearray, reference=message)

                audio_source = discord.FFmpegPCMAudio('ChatGPT.wav')
                voice_client.play(audio_source)
            else:
                await message.channel.send(responsearray, reference=message)

            self.messagearray.append({"role": "assistant", "content": responsearray})

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

async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))
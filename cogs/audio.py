# hungh

# if you can't find a variable used in this file its probably imported from here
from config import *


class audio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Use UVR to separate the vocals and instrumental from a provided file, and sends the results as mp3 files.", brief="Splits audio into vocals and instrumental using AI")
    async def acapella(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = cmd_info[0]
        with open(f'I:\\Dannybot\\cogs\\dependencies\\UVR\\audio.mp3', 'wb') as f:
            f.write(requests.get(file_url).content)
            f.close
        await ctx.send("Splitting. Please wait...")
        os.system(f"cd {UltimateVocalRemover}")
        os.chdir(f"{UltimateVocalRemover}")
        os.system('python inference.py --input audio.mp3 --gpu 0')
        os.system("ffmpeg -i audio_Instruments.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Instruments.mp3 -y")
        os.system("ffmpeg -i audio_Vocals.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Vocals.mp3 -y")
        with open(f'audio_Instruments.mp3', 'rb') as f:
            await ctx.reply(file=File(f, 'Inst.mp3'))
            f.close
        with open(f'audio_Vocals.mp3', 'rb') as f:
            await ctx.reply(file=File(f, 'Vocal.mp3'))
            f.close

async def setup(bot: commands.Bot):
    await bot.add_cog(audio(bot))
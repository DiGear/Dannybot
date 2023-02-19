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
        with open(f'{UltimateVocalRemover}\\audio.mp3', 'wb') as f:
            f.write(requests.get(file_url).content)
            f.close
        await ctx.send("Splitting. Please wait...")
        os.system(f"cd {UltimateVocalRemover}")
        os.chdir(f"{UltimateVocalRemover}")
        os.system('python inference.py --input audio.mp3 --gpu 0')
        os.system("ffmpeg -i audio_Instruments.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Instruments.mp3 -y")
        os.system("ffmpeg -i audio_Vocals.wav -vn -ar 44100 -ac 2 -b:a 192k audio_Vocals.mp3 -y")
        with open(f'audio_Instruments.mp3', 'rb') as i, open(f'audio_Vocals.mp3', 'rb') as v:
            await ctx.reply(file=File(i, 'Inst.mp3'))
            await ctx.reply(file=File(v, 'Vocal.mp3'))
            i.close
            v.close

    # i need to find a nice way to implement a viewable list of soundfonts
    @commands.command(description="Renders a midi file with a random soundfont, and sends the resulting mp3. You can also choose a specific soundfont from a list of available ones.", brief="Applies a selectable soundfont to a midi file")
    async def midislap(self, ctx, *args):
        sf2s = os.listdir(f"{dannybot}\\assets\\SF2\\")
        context = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = context[0]
        if not context[1]:
            SF2 = random.choice(sf2s)
        else:
            SF2 = context[1] + ".sf2"
        with open(f'{dannybot}\\cache\\midislap.mid', 'wb') as midi_file:
            midi_file.write(requests.get(file_url).content)
            midi_file.close
        if SF2 not in sf2s:
            await ctx.reply("Please choose a valid soundfont!")
        else:
            os.system(f"fluidsynth -ni {dannybot}\\assets\\SF2\\{SF2} {dannybot}\\cache\\midislap.mid -F {dannybot}\\cache\\midislap.flac -r 44100")
            with open(f'{dannybot}\\cache\\midislap.flac', 'rb') as f:
                await ctx.reply(file=File(f, 'midislap.flac'))
                f.close

async def setup(bot: commands.Bot):
    await bot.add_cog(audio(bot))
# hungh

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class audio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(hidden=True)
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(
        description="Flips a MIDI file upside down, relative to middle C (C5).",
        brief="Flips a MIDI file upside down",
    )
    async def midiflip(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments, "midi")
        file_url = cmd_info[0]

        with open(f"{dannybot}\\cache\\midiflip.mid", "wb") as f:
            f.write(requests.get(file_url).content)

        os.system(
            f"python NegativeHarmonizer.py {dannybot}\\cache\\midiflip.mid --tonic 60 --ignore 9 --adjust-octaves"
        )

        midi_output_path = f"{dannybot}\\cache\\midiflip_negative.mid"
        os.system(
            f"fluidsynth -ni {dannybot}\\assets\\SF2\\general.sf2 {midi_output_path} -F {dannybot}\\cache\\midislap_{ctx.message.id}.wav -r 44100"
        )

        ogg_output_path = f"{dannybot}\\cache\\midislap_{ctx.message.id}.ogg"
        os.system(
            f"ffmpeg-normalize {dannybot}\\cache\\midislap_{ctx.message.id}.wav -o {ogg_output_path} -c:a libopus -b:a 64k --keep-loudness-range-target -f"
        )

        with open(f"{dannybot}\\cache\\midiflip_negative.mid", "rb") as i, open(
            ogg_output_path, "rb"
        ) as f:
            await ctx.reply(file=File(i, "flipped.mid"))
            await ctx.reply(f"Audio preview:", file=File(f, "midislap.ogg"))

    # i need to find a nice way to implement a viewable list of soundfonts
    @commands.command(
        aliases=["nathans"],
        description="Renders a MIDI file with a random soundfont and sends the resulting audio. You can also choose a specific soundfont from a list of available ones.",
        brief="Applies a selectable soundfont to a MIDI file",
    )
    async def midislap(self, ctx, *args):
        sf2s = os.listdir(f"{dannybot}\\assets\\SF2\\")
        context = await resolve_args(ctx, args, ctx.message.attachments, "midi")

        if not args and not ctx.message.attachments:
            soundfonts_list = "\n".join(sf2.replace(".sf2", "") for sf2 in sf2s)
            await ctx.reply(
                "The list of selectable soundfonts is as follows:\n" + soundfonts_list
            )
            return

        file_url = context[0]
        SF2 = context[1] + ".sf2" if context[1] else random.choice(sf2s)
        if context[1] == "random":
            SF2 = random.choice(sf2s)
        with open(f"{dannybot}\\cache\\midislap.mid", "wb") as midi_file:
            midi_file.write(requests.get(file_url).content)

        if SF2 not in sf2s:
            await ctx.reply("Please choose a valid soundfont!")
            return

        await ctx.send(
            "Generating... Use 'd.midislap' on its own to see a list of selectable soundfonts...",
            delete_after=10,
        )

        midi_output_path = f"{dannybot}\\cache\\midislap_{ctx.message.id}.wav"
        os.system(
            f"fluidsynth -ni {dannybot}\\assets\\SF2\\{SF2} {dannybot}\\cache\\midislap.mid -F {midi_output_path} -r 44100"
        )

        ogg_output_path = f"{dannybot}\\cache\\midislap_{ctx.message.id}.ogg"
        os.system(
            f"ffmpeg-normalize {midi_output_path} -o {ogg_output_path} -c:a libopus -b:a 64k -f"
        )

        with open(ogg_output_path, "rb") as f:
            await ctx.reply(f"Midislapped with {SF2}:", file=File(f, "midislap.ogg"))


async def setup(bot: commands.Bot):
    await bot.add_cog(audio(bot))

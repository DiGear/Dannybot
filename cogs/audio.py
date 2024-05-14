# hungh

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class audio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loop = True

    @commands.command(hidden=True)
    async def join(self, ctx):
        if ctx.guild.id not in whitelist:
            await ctx.send("This server is not whitelisted for this command.")
            return
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(hidden=True)
    async def leave(self, ctx):
        if ctx.guild.id not in whitelist:
            await ctx.send("This server is not whitelisted for this command.")
            return
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(
        description="Flips a MIDI file upside down, relative to middle C (C5).",
        brief="Flips a MIDI file upside down",
    )
    async def midiflip(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments, "midi")
        file_url = cmd_info[0]
        filename = os.path.basename(file_url).split("?")[0]
        
        with open(f"{dannybot}\\cache\\{filename}", "wb") as f:
            f.write(requests.get(file_url).content)

            negative_harmonizer_cmd = [
                "python", "NegativeHarmonizer.py",
                f"{dannybot}\\cache\\{filename}",
                "--tonic", "60",
                "--ignore", "9",
                "--adjust-octaves"
            ]
            subprocess.Popen(negative_harmonizer_cmd).wait()

            midi_output_path = f"{dannybot}\\cache\\{filename.replace('.mid', '_negative.mid')}"
            fluidsynth_cmd = [
                "fluidsynth", "-ni",
                f"{dannybot}\\assets\\SF2\\general.sf2",
                midi_output_path,
                "-F",
                f"{dannybot}\\cache\\midislap_{ctx.message.id}.wav",
                "-r", "44100"
            ]
            subprocess.Popen(fluidsynth_cmd).wait()

            ogg_output_path = f"{dannybot}\\cache\\{filename.replace('.mid', f'_midislap_{ctx.message.id}.ogg')}"
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", f"{dannybot}\\cache\\midislap_{ctx.message.id}.wav",
                "-c:a", "libopus",
                "-b:a", "64k",
                ogg_output_path
            ]
            subprocess.Popen(ffmpeg_cmd).wait()

        with open(midi_output_path, "rb") as i, open(ogg_output_path, "rb") as f:
            await ctx.reply(file=File(i, filename.replace('.mid', '_flipped.mid')))
            await ctx.reply(f"Audio preview:", file=File(f, filename.replace('.mid', f'_flipped.ogg')))

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
        os.system(f"ffmpeg -i {midi_output_path} -c:a libopus -b:a 64k {ogg_output_path}")

        with open(ogg_output_path, "rb") as f:
            await ctx.reply(f"Midislapped with {SF2}:", file=File(f, "midislap.ogg"))


    @commands.command()
    async def play(self, ctx, url=None):
        if ctx.guild.id not in whitelist:
            await ctx.send("This server is not whitelisted for this command.")
            return
        current_directory = os.getcwd()
        try:
            os.chdir(f"{dannybot}\\cache")
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                voice_channel = ctx.voice_client
            else:
                try:
                    voice_channel = await channel.connect()
                except Exception as e:
                    await ctx.send(f'Unable to connect to the voice channel: {e}')
                    return
            if url is None and len(ctx.message.attachments) > 0:
                url = ctx.message.attachments[0].url
            if url is None:
                await ctx.send('Please provide a URL or attach an MP3 file.')
                return
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'force_overwrites': True,
                'no_check_certificate': True,
                'no_playlist': True,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'cookiefile': Cookies,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info_dict)
                    file_path_with_format = file_path.rsplit(".", maxsplit=1)[0] + ".mp3"
            except Exception as e:
                await ctx.send(f'An error occurred during the download process: {e}')
                return
            if voice_channel.is_playing():
                voice_channel.stop()
            voice_channel.play(discord.FFmpegPCMAudio(file_path_with_format))
            await ctx.send(f'Now playing: `{info_dict["title"]}`')

        finally:
            os.chdir(current_directory)

async def setup(bot: commands.Bot):
    await bot.add_cog(audio(bot))
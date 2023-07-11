# idk what other cog to put these in - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="8ball", description="Ask Dannybot a question and he will respond with one of many answers.", brief="Ask a question and get an answer")
    async def _8ball(self, ctx: commands.Context, *, question: str):
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(ball_responses)}')

    @commands.hybrid_command(name='logo', description="Use a custom flamingtext.com api to generate logos using random presets.", brief="Generate a logo with a random font.")
    async def logo(self, ctx: commands.Context, *, logotext: typing.Optional[str] = "Your Text Here"):
        logotype = random.choice(logolist)
        url = furl.furl(f"https://flamingtext.com/net-fu/proxy_form.cgi?script={logotype}-logo&text={logotext}&_loc=generate&imageoutput=true").url
        with urllib.request.urlopen(url) as response:
            image_bytes = response.read()
        filename = "logo_out.png"
        with open(f"{dannybot}/cache/{filename}", 'wb') as f:
            f.write(image_bytes)
        await ctx.reply(file=File(f"{dannybot}/cache/{filename}"), mention_author=True)
        
    @commands.hybrid_command(name='undertext', description="Generate a custom Undertale-Styled textbox by defining the character and text to be said.", brief="Generate a custom Undertale-Styled textbox", hidden=True)
    async def undertext(self, ctx: commands.Context, character: str, *, text: str, animated: typing.Optional[bool] = False):
        await ctx.defer()
        charname, chartext, animated = undertext(character, text, animated)
        url = furl.furl(f"https://www.demirramon.com/gen/undertale_text_box.{'gif' if animated else 'png'}?text={chartext}&character={charname}{'&animate=true' if animated else ''}").url
        with urllib.request.urlopen(url) as response:
            image_bytes = response.read()
        filename = f"undertext_out.{'gif' if animated else 'png'}"
        with open(f"{dannybot}/cache/{filename}", 'wb') as f:
            f.write(image_bytes)
        await ctx.reply(file=discord.File(f"{dannybot}/cache/{filename}"), mention_author=True)

    @commands.command(hidden=True)
    async def bugle(self, ctx):
        with open(f"{dannybot}\\assets\\bugle.png", "rb") as f:
            await ctx.reply(file=File(f, "dumbass.png"), mention_author=True)

    @commands.hybrid_command(name="download", aliases=["dl", "ytdl", "down"], description="Download from a multitude of sites in audio or video format.", brief="Download from a list of sites as mp3 or mp4")
    async def download(self, ctx: commands.Context, file_download: str, format: typing.Optional[Literal['mp3', 'ogg', 'mp4', 'webm']] = 'mp3'):
        await ctx.send('Ok. Downloading...')

        video_formats = ['mp4']
        audio_formats = ['mp3']
        os.chdir(f"{dannybot}\\cache")

        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'force_overwrites': True,
                'no_check_certificate': True,
                'no_playlist': True
            }

            if format in video_formats:
                ydl_opts['format'] = format
            elif format in audio_formats:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format,
                    'preferredquality': '192',
                }]
            else:
                await ctx.reply("The format specified is invalid. Please use `mp4, webm` for video, or `mp3, flac, wav, ogg` for audio.")
                return

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:        
                    info_dict = ydl.extract_info(file_download, download=True)
                    file_path = ydl.prepare_filename(info_dict)
                    # Modify the file extension based on the specified format
                    file_path_with_format = file_path.rsplit('.', maxsplit=1)[0] + f".{format}"
                except:
                    file_path_with_format = (f"non-ytdl.{format}")

            await ctx.reply(file=discord.File(file_path_with_format))
        except Exception as e:
            logging.exception("An error occurred during the download process:")
            await ctx.reply(f"An error occurred during the download process: {e}")
        finally:
            os.chdir(f"{dannybot}")

async def setup(bot: commands.Bot):
    await bot.add_cog(misc(bot))
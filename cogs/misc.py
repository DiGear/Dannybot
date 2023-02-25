# idk what other cog to put these in - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *


class misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="8ball", description="Ask Dannybot a question and he will respond with one of many answers.", brief="Ask a question and get an answer")
    async def _8ball(self, ctx, *, question):
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(ball_responses)}')

    @commands.command(description="Use a custom flamingtext.com api to generate logos using random presets.", brief="Generate a logo with a random font.")
    async def logo(self, ctx, *, logotext: typing.Optional[str] = "Your Text Here"):
        # choose a random type from the array
        logotype = random.choice(logolist)

    # add the text to the end of a flamingtext image url
        url = furl.furl(f"https://flamingtext.com/net-fu/proxy_form.cgi?script={logotype}-logo&text={logotext}&_loc=generate&imageoutput=true").url
        image = urllib.request.URLopener()
        image.retrieve(url, f"{dannybot}\\cache\\logo_out.png")

        await ctx.reply(file=File(f"{dannybot}\\cache\\logo_out.png"), mention_author=True)

    @commands.command(description="Generate a custom Undertale-Styled textbox by defining the character and text to be said.", brief="Generate a custom Undertale-Styled textbox")
    async def undertext(self, ctx, CharacterName, *, Text):
        charname, chartext, animated = undertext(CharacterName, Text, False)
        if not animated:
            url = furl.furl(f"https://www.demirramon.com/gen/undertale_text_box.png?text={chartext}&character={charname}").url
            image = urllib.request.URLopener()
            image.retrieve(url, f"{dannybot}\\cache\\undertext_out.png")
            await ctx.reply(file=File(f"{dannybot}\\cache\\undertext_out.png"), mention_author=True)
            return
        else:
            url = furl.furl(f"https://www.demirramon.com/gen/undertale_text_box.gif?text={chartext}&character={charname}&animate=true").url
            image = urllib.request.URLopener()
            image.retrieve(url, f"{dannybot}\\cache\\undertext_out.gif")
            await ctx.reply(file=File(f"{dannybot}\\cache\\undertext_out.gif"), mention_author=True)
            return

    @commands.command(description="Download from a multitude of sites in mp3, flac, wav, or ogg audio; or download as an mp4 file. The supported sites are listed at https://ytdl-org.github.io/youtube-dl/supportedsites.html", brief="Download from a list of sites as mp3 or mp4")
    async def download(self, ctx, file_download, format='mp3'):
        clear_cache() # this is not how bugs should be fixed but 🖕
        await ctx.send('Ok. Downloading...')
        # defines
        file_download = file_download.split("&")[0]
        video_formats = ['mp4', 'webm']
        audio_formats = ['mp3', 'ogg', 'flac', 'wav']

        os.chdir(f"{dannybot}\\cache")

        try:
            if format in video_formats:
                os.system(f'"yt-dlp -o "ytdl.%(ext)s" --no-check-certificate --no-playlist -f {format} {file_download}"')
            elif format in audio_formats:
                os.system(f'"yt-dlp -o "ytdl.%(ext)s" --no-check-certificate --no-playlist --audio-format {format} -x {file_download}"')
            else:
                await ctx.reply("The format specified is invalid. Please use `mp4, webm` for video, or `mp3, flac, wav, ogg` for audio.")
        except:
            os.chdir(f"{dannybot}")

        await ctx.reply(file=discord.File(f'ytdl.{format}'))
        os.chdir(f"{dannybot}")

async def setup(bot: commands.Bot):
    await bot.add_cog(misc(bot))

# this is where the shit hits the fan, pretty much

# if you can't find a variable used in this file its probably imported from here
from config import *


class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext", brief="Turns an image into an impact font meme")
    async def meme(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        
        # distinquish between command arguments and command file uploads
        context = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = context[0]
        meme_text = context[1]
        
        # gif files suck!
        if '.gif' in file_url or 'https://tenor.com/' in file_url:
            is_gif = True
        else:
            is_gif = False
        
        # this downloads the image to be meme'd and then configures all of the args appropriately
        with open(f"{dannybot}\\cache\\meme_in.png", 'wb') as f:
                    f.write(requests.get(file_url).content)
                    f.close
        png_path = (f"{dannybot}\\cache\\meme_in.png")

        # split the meme text by top and bottom and then capitalize it
        if ("|" in meme_text):
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0].upper()
            Bottom_Text = meme_text_splitted[1].upper()
        else:
            Top_Text = meme_text.upper()
            Bottom_Text = ""

        # determine if we need to call the standard or gif function
        if (is_gif):
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(file_url).content)
                f.close
            unpack_gif(f"{dannybot}\\cache\\gif.gif")
            make_meme_gif(Top_Text, Bottom_Text)
            repack_gif()
        else:
            make_meme(Top_Text, Bottom_Text, png_path)

        # determine if we need to send a gif or png in response
        if (is_gif):
            with open(f"{dannybot}\\cache\\ffmpeg_out.gif", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            with open(f"{dannybot}\\cache\\meme_out.png", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.png'), mention_author=True)
                f.close


async def setup(bot: commands.Bot):
    await bot.add_cog(image(bot))
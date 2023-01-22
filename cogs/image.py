# this is where the shit hits the fan, pretty much - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *


class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # i have a feeling im making this more complicated than it needs to be - FDG
    @commands.command(description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext", brief="Turns an image into an impact font meme")
    async def meme(self, ctx, *args):
        
        # distinquish between command arguments and command file uploads
        context = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = context[0]
        meme_text = context[1]
        
        # gif files suck! - FDG
        if '.gif' in file_url or 'https://tenor.com/' in file_url:
            is_gif = True
        else:
            is_gif = False

        # prepare the meme text for the api
        meme_text = jacebrowning_encode(meme_text)
        print(meme_text)

        # split the meme text by top and bottom and then capitalize it
        if ("|" in meme_text):
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0].upper()
            Bottom_Text = meme_text_splitted[1].upper()
        else:
            Top_Text = meme_text.upper()
            Bottom_Text = "_"
        
        # final encoding step
        if Top_Text == "":
            Top_Text = "_"
        if Bottom_Text == "":
            Bottom_Text = "_"

        # determine if we need to call the standard function or gif function
        if (is_gif):
            url = f"https://api.memegen.link/images/custom/{Top_Text}/{Bottom_Text}.gif?background={file_url}&font=impact"
            await ctx.reply(url, mention_author=True)
        else:
            url = f"https://api.memegen.link/images/custom/{Top_Text}/{Bottom_Text}.png?background={file_url}&font=impact"
            await ctx.reply(url, mention_author=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(image(bot))
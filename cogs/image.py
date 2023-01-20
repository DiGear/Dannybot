# this is where the shit hits the fan, pretty much
import typing

import requests
from discord import File
from discord.ext import commands

# if you can't find a variable used in this file its probably imported from here
from data import *


class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext", brief="Turns an image into an impact font meme")
    async def meme(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        # ezogaming shit
        # this downloads the image to be meme'd and then configures all of the args appropriately
        # there has to be a better way to do this
        with open(f"{dannybot}\\cache\\meme_in.png", 'wb') as f:
            try:
                f.write(requests.get(context).content)
                f.close
            except:
                if ctx.message.attachments:
                    meme_text_Fallback_Value = context
                    meme_text = context + " " + meme_text
                    if ("ValueError" in meme_text):
                        meme_text = meme_text_Fallback_Value
                    context = ctx.message.attachments[0].url
                    f.write(requests.get(context).content)
                    f.close
                else:
                    meme_text_Fallback_Value = context
                    meme_text = context + " " + meme_text
                    if ("ValueError" in meme_text):
                        meme_text = meme_text_Fallback_Value
                    context = await message_history_img_handler(ctx)
                    f.write(requests.get(context).content)
                    f.close
        # end ezogaming shit
        # split the meme text by top and bottom
        if ("|" in meme_text):
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0].upper()
            Bottom_Text = meme_text_splitted[1].upper()
        else:
            Top_Text = meme_text.upper()
            Bottom_Text = ""
        # display it in console for debugging purposes
        print("Top_Text is: [" + Top_Text + "]")
        print("Bottom_Text is: [" + Bottom_Text + "]")
        png_path = (f"{dannybot}\\cache\\meme_in.png")
        # determine if we need to call the standard or gif function
        if '.gif' not in context:
            make_meme(Top_Text, Bottom_Text, png_path)
        else:
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(context).content)
                f.close
            unpack_gif(f"{dannybot}\\cache\\gif.gif")
            make_meme_gif(Top_Text, Bottom_Text)
            repack_gif()
        # determine if we need to send a gif or png in response
        if '.gif' in context:
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
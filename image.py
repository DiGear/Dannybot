# this is where the shit hits the fan, pretty much
import typing

import requests
from discord import File
from discord.ext import commands

from data import *


class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext",
        brief="Turns an image into an impact font meme"
    )
    async def meme(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
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
        try:
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0]
            Bottom_Text = meme_text_splitted[1]
        except:
            Top_Text = meme_text
            Bottom_Text = ""
        Top_Text = Top_Text.upper()
        Bottom_Text = Bottom_Text.upper()
        png_path = (f"{dannybot}\\cache\\meme_in.png")
        gif_path = None
        is_gif = None
        print("Top_Text is: [" + Top_Text + "]")
        print("Bottom_Text is: [" + Bottom_Text + "]")

        if '.gif' in context:
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(context).content)
                f.close
            unpack_gif(f"{dannybot}\\cache\\gif.gif")
        if '.gif' not in context:
            is_gif = False
            make_meme(Top_Text, Bottom_Text, png_path, is_gif)
        else:
            is_gif = True
            make_meme(Top_Text, Bottom_Text, png_path, is_gif)
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

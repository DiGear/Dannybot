# this is where the shit hits the fan, pretty much

import urllib
import urllib.request

import furl
from discord import File
from discord.ext import commands

# if you can't find a variable used in this file its probably imported from here
from data import *


class misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        description="Generate a custom Undertale-Styled textbox by defining the character and text to be said.",
        brief="Generate a custom Undertale-Styled textbox"
    )
    async def undertext(self, ctx, CharacterName, *, Text):
        if(Text.endswith("_ _")):
            Text = "%20"
        url = ("https://www.demirramon.com/gen/undertale_text_box.png?text=" +
               str(Text) + "&character=" + str(undertext(CharacterName)))
        url = furl.furl(url).url
        image = urllib.request.URLopener()
        print(url)
        image.retrieve(url, f"{dannybot}\\cache\\undertext_out.png")

        await ctx.reply(file=File(f"{dannybot}\\cache\\undertext_out.png"), mention_author=True)

    @commands.command(
        description="Generate a custom Deltarune-Styled textbox by defining the character and text to be said.",
        brief="Generate a custom Deltarune-Styled textbox"
    )
    async def deltatext(self, ctx, CharacterName, *, Text):
        if(Text.endswith("_ _")):
            Text = "%20"
        url = ("https://www.demirramon.com/gen/undertale_text_box.png?text=" + str(Text) +
               "&mode=darkworld&box=deltarune&character=" + str(undertext(CharacterName)))
        url = furl.furl(url).url
        image = urllib.request.URLopener()
        image.retrieve(url, f"{dannybot}\\cache\\deltatext_out.png")

        await ctx.reply(file=File(f"{dannybot}\\cache\\deltatext_out.png"), mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(misc(bot))

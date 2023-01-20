# this is where the shit hits the fan, pretty much

import typing
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
        Name = str(undertext(CharacterName))
        # allow for blank textbox generation
        if(Text.endswith("_ _")):
            Text = "%20"
        url = furl.furl(f"https://www.demirramon.com/gen/undertale_text_box.png?text={Text}&character={Name}").url
        image = urllib.request.URLopener()
        image.retrieve(url, f"{dannybot}\\cache\\undertext_out.png")

        await ctx.reply(file=File(f"{dannybot}\\cache\\undertext_out.png"), mention_author=True)

    @commands.command(description="Generate a custom Deltarune-Styled textbox by defining the character and text to be said.", brief="Generate a custom Deltarune-Styled textbox")
    async def deltatext(self, ctx, CharacterName, *, Text):
        Name = str(undertext(CharacterName))
        # allow for blank textbox generation
        if(Text.endswith("_ _")):
            Text = "%20"
        url = furl.furl(f"https://www.demirramon.com/gen/undertale_text_box.png?text={Text}&mode=darkworld&box=deltarune&character={Name}").url
        url = furl.furl(url).url
        image = urllib.request.URLopener()
        image.retrieve(url, f"{dannybot}\\cache\\deltatext_out.png")

        await ctx.reply(file=File(f"{dannybot}\\cache\\deltatext_out.png"), mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(misc(bot))

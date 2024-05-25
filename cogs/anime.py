import logging
from config import *

logger = logging.getLogger(__name__)


class anime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_anime_action(
        self, ctx: commands.Context, action: str, member: discord.Member
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://nekos.life/api/v2/img/{action}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("url")
        if action == "kiss":
            action = "kisse"
        embed = discord.Embed(
            description=(
                f"## {ctx.author.display_name} {action}s {member.display_name}"
                if member != ctx.author
                else f"# {ctx.author.display_name} {action}s themself"
            ),
            color=discord.Color(random.randint(0, 0xFFFFFF)),
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="tickle",
        description="tickles the Recipient (or yourself).",
        brief="tickles the Recipient (or yourself).",
    )
    async def tickle(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "tickle", member)

    @commands.hybrid_command(
        name="feed",
        description="feeds the Recipient (or yourself).",
        brief="feeds the Recipient (or yourself).",
    )
    async def feed(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "feed", member)

    @commands.hybrid_command(
        name="slap",
        description="slaps the Recipient (or yourself).",
        brief="slaps the Recipient (or yourself).",
    )
    async def slap(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "slap", member)

    @commands.hybrid_command(
        name="pat",
        description="pats the Recipient (or yourself).",
        brief="pats the Recipient (or yourself).",
    )
    async def pat(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "pat", member)

    @commands.hybrid_command(
        name="kiss",
        description="kisses the Recipient (or yourself).",
        brief="kisses the Recipient (or yourself).",
    )
    async def kiss(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "kiss", member)

    @commands.hybrid_command(
        name="cuddle",
        description="cuddles the Recipient (or yourself).",
        brief="cuddles the Recipient (or yourself).",
    )
    async def cuddle(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "cuddle", member)

    @commands.hybrid_command(
        name="hug",
        description="hugs the Recipient (or yourself).",
        brief="hugs the Recipient (or yourself).",
    )
    async def hug(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        await self.send_anime_action(ctx, "hug", member)


async def setup(bot: commands.Bot):
    await bot.add_cog(anime(bot))
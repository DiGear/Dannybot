# this just has stuff for gathering user info

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class user(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="avatar",
        description="Grab the command users avatar, and send it.",
        brief="Display provided users avatar(s)",
    )
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        if member.guild_avatar:
            embed = discord.Embed()
            embed.set_image(url=str(member.avatar.url))
            await ctx.send(
                f"Avatar of {member.display_name}.", mention_author=True, embed=embed
            )
            embed = discord.Embed()
            embed.set_image(url=str(member.guild_avatar.url))
            await ctx.send(
                f"Server Avatar of {member.display_name}.",
                mention_author=True,
                embed=embed,
            )
        else:
            embed = discord.Embed()
            embed.set_image(url=str(member.avatar.url))
            await ctx.send(
                f"Avatar of {member.display_name}.", mention_author=True, embed=embed
            )

    @commands.hybrid_command(
        name="info",
        description="Grab the users account information, and then send it in an embed.",
        brief="Display provided users information",
    )
    async def info(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        date_format = "%#d, %B, %Y at %I:%M %p UTC"
        embed_info = {
            "title": "User Information",
            "thumbnail": {"url": member.avatar.url},
            "fields": [
                {
                    "name": "Display name:",
                    "value": f"{member.global_name}",
                    "inline": False,
                },
                {"name": "Username:", "value": f"{member.name}", "inline": False},
                {"name": "Server Name:", "value": member.display_name, "inline": False},
                {"name": "ID:", "value": member.id, "inline": False},
                {"name": "Status:", "value": member.raw_status},
                {"name": "Is active on mobile:", "value": member.is_on_mobile()},
                {"name": "Is Bot account:", "value": member.bot},
                {
                    "name": "Account Creation Date:",
                    "value": member.created_at.strftime(date_format),
                    "inline": False,
                },
                {
                    "name": "Server Join Date:",
                    "value": member.joined_at.strftime(date_format),
                    "inline": False,
                },
            ],
            "footer": {"text": f"Command ran on {member.guild}."},
        }
        embed = discord.Embed.from_dict(embed_info)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(user(bot))

# this just has stuff for gathering user info

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)


class user(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    @commands.hybrid_command(name='avatar', description="Grab the command users avatar, and send it.", brief="Display provided users avatar(s)")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        
        if member.guild_avatar:
            embed = discord.Embed()
            embed.set_image(url=str(member.avatar.url))
            await ctx.send(f"Avatar of {member.display_name}.", mention_author=True, embed=embed)
            embed = discord.Embed()
            embed.set_image(url=str(member.guild_avatar.url))
            await ctx.send(f"Server Avatar of {member.display_name}.", mention_author=True, embed=embed)
        else:
            embed = discord.Embed()
            embed.set_image(url=str(member.avatar.url))
            await ctx.send(f"Avatar of {member.display_name}.", mention_author=True, embed=embed)

    @commands.hybrid_command(name='info', description="Grab the users account information, and then send it in an embed.", brief="Display provided users information")
    async def info(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Display name:", value=f"{member.global_name}", inline=False)
        embed.add_field(name="Username:", value=f"{member.name}", inline=False)
        embed.add_field(name="Server Name:", value=str(member.display_name), inline=False)
        embed.add_field(name="ID:", value=str(member.id), inline=False)
        embed.add_field(name="Status:", value=str(member.raw_status))
        embed.add_field(name="Is active on mobile:", value=str(member.is_on_mobile()))
        embed.add_field(name="Is Bot account:", value=str(member.bot))
        embed.add_field(name="Account Creation Date:", value=member.created_at.strftime("%#d, %B, %Y at %I:%M %p UTC"), inline=False)
        embed.add_field(name="Server Join Date:", value=member.joined_at.strftime("%#d, %B, %Y at %I:%M %p UTC"), inline=False)
        embed.set_footer(text=f"Command ran on {member.guild}.")
        await ctx.reply(embed=embed, mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(user(bot))
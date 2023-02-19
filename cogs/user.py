# this just has stuff for gathering user info

# if you can't find a variable used in this file its probably imported from here
from config import *


class user(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Grab the command author's avatar, and send it. If a User ID or @Mention is provided. Send their avatar(s) instead.", brief="Display provided users avatar(s)")
    async def avatar(self, ctx, member: discord.Member = None):
        # this checks if a member was mentioned by an @ or by It, if not, it uses the Authors ID
        member = ctx.author if not member else member
        embed = discord.Embed(color=0xffb6c1)  # generate embed
        embed.set_image(url=str(member.avatar.url))  # grab the URL
        await ctx.reply("Avatar of " + str(member.display_name) + ".", mention_author=True)
        await ctx.send(embed=embed)  # send embed
        print("grabbed avatar of " + str(member.display_name))
    
    @commands.command(description="Grab the command author's banner(s), and send it. If a User ID or @Mention is provided. Send their banner instead.", brief="Display provided users banner(s)" )
    async def banner(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        user = await self.bot.fetch_user(member.id)
        banner_url = user.banner.url
        await ctx.send(f"{banner_url}")

    @commands.command(description="Grab the command author's account information, and then send it in an embed. If a User ID or @Mention is provided. Send their account information instead.", brief="Display provided users information")
    async def info(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        perms = '\n'.join(
            perm for perm, value in member.guild_permissions if value)
        embed = discord.Embed(title="User Information", color=0xffb6c1)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Discord Name:", value=str(
            member.name) + "#" + (member.discriminator), inline=False)
        embed.add_field(name="ID:", value=str(member.id), inline=False)
        embed.add_field(name="Is Bot Account:", value=str(member.bot))
        embed.add_field(name="Account Creation Date:", value=member.created_at.strftime(
            "%#d, %B, %Y at %I:%M %p UTC"), inline=False)
        embed.add_field(name="Server Nickname:", value=str(
            member.display_name), inline=False)
        embed.add_field(name='Server Permissions:', value=perms)
        embed.set_footer(text="Command ran on " + str(member.guild) + ".")
        await ctx.reply(embed=embed, mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(user(bot))

from config import *
import logging
import random

logger = logging.getLogger(__name__)
arrow_emojis = ["⬅️", "➡️"]

class booru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_msg = None

    #gelbooru
    @commands.hybrid_command(name="gelbooru", aliases=["gel"], description="Browse gelbooru posts using the bot.", brief="Browse gelbooru posts using the bot.")
    async def gelbooru(self, ctx: commands.Context, *, tag: str):
        payload = {'tags': tag, 'limit': 10000, 'pid': 0}

        async with ClientSession() as session:
            async with session.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index', params=payload) as response:
                tree = ElementTree.parse(BytesIO(await response.read()))

        posts = list(tree.iterfind('.//post'))
        if not posts: return await ctx.send(f'No results found for {tag}.')

        random.shuffle(posts)
        if self.last_msg: await self.last_msg.clear_reactions()
        current_index = 0
        self.last_msg = await self.send_valid_post(ctx, posts, current_index) or self.last_msg
        if self.last_msg:
            for emoji in arrow_emojis:
                try:
                    await self.last_msg.add_reaction(emoji)
                except AttributeError:
                    await ctx.send('No valid posts found')
                    async for msg in ctx.channel.history(limit=1):
                        return await msg.clear_reactions()
                
        while True:
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=self.reaction_check(ctx, self.last_msg))
                current_index += self.reaction_index(react)
                current_index = max(0, min(len(posts) - 1, current_index))                
                await self.last_msg.remove_reaction(react.emoji, user)
                if 0 <= current_index < len(posts):
                    new_embed = await self.send_valid_post(ctx, posts, current_index, True)
                    await self.last_msg.edit(embed=new_embed)                
            except asyncio.TimeoutError:
                try: await self.last_msg.clear_reactions()
                except: pass
                break

    def reaction_check(self, ctx, msg):
        return lambda react, user: user == ctx.author and str(react.emoji) in arrow_emojis and react.message.id == msg.id

    def reaction_index(self, react):
        return 1 if str(react) == arrow_emojis[1] else -1 
    
    async def send_valid_post(self, ctx, posts, idx, return_embed=False):
        while idx < len(posts):
            rating = posts[idx].find('rating').text
            if rating in ('explicit') and not (ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel)):
                idx += 1
            else:
                return await self.send_embed(ctx, posts[idx], return_embed)
            await ctx.send('No valid posts found')
            async for msg in ctx.channel.history(limit=1):
                return await msg.clear_reactions()

    async def send_embed(self, ctx, post, return_embed=False):
        id_ = post.find('id').text
        file_url = post.find('file_url').text
        tags = ', '.join(post.find('tags').text.split())[:2000]

        embed = discord.Embed(title=f"Gelbooru",url=f"https://gelbooru.com/index.php?page=post&s=view&id={id_}")
        embed.set_image(url=file_url)
        embed.add_field(name='Tags', value=tags, inline=False)

        return embed if return_embed else await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(booru(bot))
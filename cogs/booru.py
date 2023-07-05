# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class booru(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_index = 0
        self.message = None
        self.embed = None
        self.reaction_task = None
    
    @staticmethod
    def get_image_url(post):
        if post:
            image_url = post.get('file_url')
            if not image_url:
                return None
            return image_url
        
    @staticmethod
    def create_embed(post):
        embed = discord.Embed()
        embed.add_field(name='Artist:', value=post['artist'], inline=False)
        embed.add_field(name='Tags:', value=post['all_tags'], inline=False)
        embed.set_footer(text=f"Score: {post['score']}")
        embed.set_image(url=post['image_url'])
        return embed
    
    def update_embed(self, post):
        self.embed.remove_field(0)
        self.embed.remove_field(0)
        self.embed.add_field(name='Artist:', value=post['artist'], inline=False)
        self.embed.add_field(name='Tags:', value=post['all_tags'], inline=False)
        self.embed.set_footer(text=f"Score: {post['score']}")
        self.embed.set_image(url=post['image_url'])
    
    @commands.hybrid_command(name='danbooru', aliases=["dan"], description="Browse images on danbooru.donmai.us. Limited to 2 tags per search.", brief="Browse images from Danbooru")
    async def danbooru(self, ctx: commands.Context, *, tags):
        await ctx.defer()
        tags = tags.replace(", ", "+")
        tags = tags.replace(" ", "+")
        url = f"https://danbooru.donmai.us/posts.json?&limit=1000000&tags={tags}"
        print(url)
        response = requests.get(url)
        data = response.json()

        if 'error' in data and data['error'] == 'PostQuery::TagLimitError':
            await ctx.send("Danbooru only allows free users to search for a maximum of 2 tags.")
            return

        if not data:
            await ctx.send("No results found.")
            return

        random.shuffle(data)

        sfw_posts = [post for post in data if post.get('rating') == 'g']
        nsfw = ctx.channel.is_nsfw()
        try:
            sfw_posts = sfw_posts if not nsfw else data
            if nsfw:
                    words = ['loli', 'fetus', 'baby', 'toddler', 'rape', 'guro']
                    if any(word in tags for word in words):
                        await ctx.reply('fuck no')
                        return
        except:
            sfw_posts = sfw_posts
        total_posts = len(sfw_posts)

        self.current_index = 0
        self.message = None
        self.embed = None

        await self.show_image(ctx, sfw_posts, total_posts)

    async def show_image(self, ctx, sfw_posts, total_posts):
        if self.current_index >= total_posts:
            return

        post = sfw_posts[self.current_index]
        image_url = self.get_image_url(post)
        if not image_url:
            self.current_index += 1
            await self.show_image(ctx, sfw_posts, total_posts)
            return

        all_tags = post.get('tag_string').replace('_', '\_')[:1023]
        score = post.get('score')
        artist = post.get('tag_string_artist').replace('_', '\_')
        post_data = {
            'image_url': image_url,
            'all_tags': all_tags,
            'score': score,
            'artist': artist
        }

        if self.message:
            self.update_embed(post_data)
            await self.message.edit(embed=self.embed)
        else:
            self.embed = self.create_embed(post_data)
            self.message = await ctx.send(embed=self.embed)
            await self.message.add_reaction('⬅️')
            await self.message.add_reaction('➡️')

        def check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) in ['⬅️', '➡️']
                and reaction.message.id == self.message.id
            )

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '⬅️':
                self.current_index = max(0, self.current_index - 1)
            elif str(reaction.emoji) == '➡️':
                self.current_index = min(self.current_index + 1, total_posts - 1)

            await self.message.remove_reaction(reaction, user)

            if self.reaction_task:
                self.reaction_task.cancel()

            self.reaction_task = asyncio.create_task(self.show_image(ctx, sfw_posts, total_posts))

        except asyncio.TimeoutError:
            await self.message.clear_reactions()

async def setup(bot: commands.Bot):
    await bot.add_cog(booru(bot))
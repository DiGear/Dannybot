# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class booru(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_index = 0
        
    @commands.command(aliases=["dan"], description="Browse images on danbooru.donmai.us. Limited to 2 tags per search.", brief="Browse images from Danbooru")
    async def danbooru(self, ctx, tag1: str, tag2: str = ""):
        # Concatenate the tags
        tags = f"{tag1}+{tag2}" if tag2 else tag1

        # Send a request to Danbooru API
        url = f"https://danbooru.donmai.us/posts.json?&tags={tags}"
        response = requests.get(url)
        data = response.json()
        
        # Check if the API returned a tag limit error
        if 'error' in data and data['error'] == 'PostQuery::TagLimitError':
            await ctx.send("Danbooru only allows free users to search for a maximum of 2 tags.")
            return

        # Check if any images were found
        if not data:
            await ctx.send("No results found.")
            return
        
        random.shuffle(data)
        
        # Retrieve the image URL
        if ctx.channel.is_nsfw():
            post = data[0] if data else None
        else:
            sfw_posts = [post for post in data if post.get('rating') == 'g']
            post = sfw_posts[0]

        if post:
            image_url = post.get('file_url')
                # Check if the URL is present
            if not image_url:
                # Try to find another image
                return await self.danbooru(ctx, tag1, tag2)
            all_tags = post.get('tag_string').replace('_','\_')[:1023]
            score = post.get('score')
            artist = post.get('tag_string_artist').replace('_','\_')
            
        # Check if the URL is well-formed
        try:
            if not image_url.startswith("http"):
                await ctx.send("An error occurred while fetching the image.")
                return
        except:
           await ctx.send("An error occurred while fetching the image.") 
           return
        
        # Create a Discord embed
        embed = discord.Embed()
        embed.add_field(name='Artist:', value=f"{artist}", inline=True)
        embed.add_field(name='Tags:', value=f"{all_tags}", inline=True)
        embed.set_footer(text=f"Score: {score}")

        # Set the image URL
        embed.set_image(url=image_url)

        # Send the embed to the channel
        message = await ctx.send(embed=embed)

        # Add arrow reaction emotes
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) in ['⬅️', '➡️']
                and reaction.message.id == message.id
            )

        while True:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '⬅️':
                    if self.current_index > 0:
                        self.current_index -= 1
                elif str(reaction.emoji) == '➡️':
                    self.current_index += 1

                # Retrieve the image URL from the updated index
                while True:
                    if ctx.channel.is_nsfw():
                        post = data[self.current_index] if data else None
                    else:
                        sfw_posts = [post for post in data if post.get('rating') == 'g']
                        post = sfw_posts[self.current_index]
                    image_url = post.get('file_url')
                    if not image_url:
                        self.current_index += 1
                        post = data[self.current_index]
                        continue
                    all_tags = post.get('tag_string').replace('_','\_')[:1023]
                    score = post.get('score')
                    artist = post.get('tag_string_artist').replace('_','\_')
                    
                    # Update the embed with the new contents
                    embed.remove_field(0)
                    embed.remove_field(0)
                    embed.add_field(name='Artist:', value=f"{artist}", inline=True)
                    embed.add_field(name='Tags:', value=f"{all_tags}", inline=True)
                    embed.set_footer(text=f"Score: {score}")
                    embed.set_image(url=image_url)

                    # Update the message content with the updated embed
                    await message.edit(content=None, embed=embed)
                    await message.remove_reaction(reaction, user)
                    break

            except asyncio.TimeoutError:
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(booru(bot))
# yeezy asked - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class Google(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='google', aliases=["g"], description="Browse images on Google.com", brief="Browse images from Google")
    @commands.has_permissions(manage_messages=True)
    async def google(self, ctx: commands.Context, *, query: str):
        await ctx.defer()
        gis = GoogleImagesSearch(google_api_key, google_cx_key)

        class ImagePaginator:
            def __init__(self, ctx, gis, query):
                self.ctx = ctx
                self.gis = gis
                self.query = query
                self.message = None
                self.embed = None
                self.current_index = 0
                self.reaction_task = None
                self.total_results = 0  # Total number of results

            def create_embed(self, result):
                # Create an embed with the image URL and page information
                embed = discord.Embed(title='Google Image Search', color=discord.Color.blue())
                embed.set_image(url=result.url)
                embed.set_footer(text=f'Page {self.current_index + 1}/{self.total_results}')
                return embed

            async def show_image(self):
                try:
                    # Perform the image search using the GoogleImagesSearch object
                    self.gis.search({'q': self.query, 'num': 50})

                    # Retrieve the search results
                    results = self.gis.results()

                    if not results:
                        # If no results found, send a message and return
                        await self.ctx.send("No results found.")
                        return

                    self.current_index = 0
                    self.total_results = len(results)  # Calculate the total results count

                    self.embed = self.create_embed(results[self.current_index])

                    if self.message:
                        # If there is already a message, edit it with the new embed
                        await self.message.edit(embed=self.embed)
                    else:
                        # If no existing message, send a new message with the embed
                        self.message = await self.ctx.send(embed=self.embed)
                        # Add reaction buttons to navigate through the images
                        await self.message.add_reaction('⬅️')
                        await asyncio.sleep(1)
                        await self.message.add_reaction('➡️')

                    def check(reaction, user):
                        # Check if the reaction is from the original author and a valid emoji
                        return (
                            user == self.ctx.author
                            and str(reaction.emoji) in ['⬅️', '➡️']
                            and reaction.message.id == self.message.id
                        )

                    while True:
                        # Wait for a reaction from the original author
                        reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)

                        if str(reaction.emoji) == '⬅️':
                            # If left arrow clicked, decrement the current index
                            self.current_index = max(0, self.current_index - 1)
                        elif str(reaction.emoji) == '➡️':
                            # If right arrow clicked, increment the current index
                            self.current_index = min(self.current_index + 1, self.total_results - 1)

                        await self.message.remove_reaction(reaction, user)

                        # Update the embed with the new image and page information
                        self.embed = self.create_embed(results[self.current_index])
                        await self.message.edit(embed=self.embed)

                except asyncio.TimeoutError:
                    # If no reaction received within the timeout, clear reactions
                    await self.message.clear_reactions()
                except Exception as e:
                    # Log any other exceptions that occurred during image search
                    logger.error(f"An error occurred during image search: **{str(e)}**")

        # Create an instance of ImagePaginator and display the image results
        paginator = ImagePaginator(ctx, gis, query)
        try:
            await paginator.show_image()
        except Exception as e:
            # Log any exceptions that occurred during image search command
            logger.error(f"An error occurred in the 'image' command: **{str(e)}**")


async def setup(bot: commands.Bot):
    await bot.add_cog(Google(bot))
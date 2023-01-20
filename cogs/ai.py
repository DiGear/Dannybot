# most of these are APIs

# if you can't find a variable used in this file its probably imported from here
from config import *

# this shit is dumb i wanna find a better way
global request_is_processing
request_is_processing = False

class ai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def dalle(self, ctx, *, prompt):
        # rotty shit
        images = None
        attempt = 0
        print("-------------------------------------")
        print(f'Dalle command ran with prompt "{prompt}"')
        while not images:
            if attempt > 0:
                print(
                    f'Image generate request failed on attempt {attempt} for prompt "{prompt}"'
                )
            attempt += 1
            images = await generate_images(prompt)
            print(
                f'Successfully started image generation with prompt "{prompt}" on attempt {attempt}'
            )
            prompt_hyphenated = prompt.replace(" ", "-")
            collage = await make_collage(images, 3)
            b = collage
            collage = discord.File(
                collage, filename=f"{prompt_hyphenated}.{DALLE_FORMAT}")
            print("Sending image...")
            await ctx.reply(file=collage, mention_author=True)
            print("Caching image...")
            with open(f"{dannybot}\\cache\\dalle.png", "wb") as f:
                b.seek(0)
                f.write(b.read())
                f.close
                print("Image Cache successful")
                print("-------------------------------------")

async def setup(bot: commands.Bot):
    await bot.add_cog(ai(bot))

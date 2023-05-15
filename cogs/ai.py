# most of these are APIs

# if you can't find a variable used in this file its probably imported from here
from config import *

# this shit is kind of dumb i wanna find a better way to do this - FDG
global request_is_processing
request_is_processing = False
logger = logging.getLogger(__name__)

class ai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['gpt'], description="Interact with GPT3 using Dannybot.", brief="Get AI generated text based on provided prompts")
    async def write(self, ctx, *, prompt):
        try:        
            gpt_prompt = str(f"write me {prompt}")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=gpt_prompt,
                temperature=random.uniform(0., 1.0),
                max_tokens=256,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            await ctx.reply(response['choices'][0]['text'], mention_author=True)
        except Exception as e:
            await ctx.send(f"An error occurred while generating the text: {str(e)}")
        
    @commands.command(description="Interact with GPT3 using Dannybot.", brief="Get AI generated text based on provided prompts")
    async def gpttemp(self, ctx, temp: typing.Optional[float] = 0.7, *, prompt):
        try:
            gpt_prompt = str(prompt)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=gpt_prompt,
                temperature=temp,
                max_tokens=256,
                top_p=1.0,
                frequency_penalty=1.0,
                presence_penalty=0.0
            )
            await ctx.reply(response['choices'][0]['text'], mention_author=True)
        except Exception as e:
            await ctx.send(f"An error occurred while generating the text: {str(e)}")

    @commands.command(aliases=['upscale'], description="Locally run waifu2x using speed-optimized settings and send the results.", brief="Upscale images using waifu2x")
    async def waifu(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Upscaling. Please wait...")
        try:
            with open(f'{dannybot}\\cache\\w2x_in.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
            os.system(f"{Waifu2x} -i {dannybot}\\cache\\w2x_in.png -o {dannybot}\\cache\\w2x_out.png -m noise_scale --scale_ratio 2 --noise_level 2 -x")
            with open(f'{dannybot}\\cache\\w2x_out.png', 'rb') as f:
                await ctx.reply(file=File(f, 'waifu2x.png'))
        except Exception as e:
            await ctx.send(f"An error occurred while upscaling the image: {str(e)}")

    @commands.command(aliases=['15', '15tts'], description="Sends AI sentences using a very real and legitimate 15.ai API.", brief="Use 15.ai to generate funny sentences")
    async def fifteen(self, ctx, *, msg):
        def check(msg):
            return msg.author == ctx.author
        global request_is_processing
        blacklist = [1, 2]
        if ctx.author.id in blacklist:
            await ctx.send("You've been blacklisted from this command")
            return
        else:
            if request_is_processing is True:
                await ctx.reply(
                    "Please allow the previous synthesis to finish.",
                    delete_after=10,
                    mention_author=True,
                )
                return
            try:
                await ctx.send('Which voice would you like? (It is case sensitive!)')
                msgfunc = await self.client.wait_for("message", check=check, timeout=30)
                requested_speaker = msgfunc.content
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")
                return
            await ctx.send("Processing... This could take a while...")
            request_is_processing = True
        FifteenAPI().save_to_file(f"{requested_speaker}", f"{msg}", f"{dannybot}\\cache\\15_output.wav")
        await ctx.reply(file=discord.File(f"{dannybot}\\cache\\15_output.wav"), mention_author=True)
        await ctx.send("This command is powered by 15.ai ^^^ https://twitter.com/fifteenai")
        request_is_processing = False
        return

    @commands.command(aliases=['quote'], description="Sends AI generated quotes using the inspirobot API.", brief="Get AI generated inspirational posters")
    async def inspire(self, ctx):
        link = "http://inspirobot.me/api?generate=true"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    if response.status == 200:
                        File_Url = await response.text()
                        async with session.get(File_Url) as image_response:
                            if image_response.status == 200:
                                image_data = await image_response.read()
                                with open(f"{dannybot}\\cache\\quote.jpg", "wb") as f:
                                    f.write(image_data)

                                f = discord.File(f"{dannybot}\\cache\\quote.jpg", filename="quote.jpg")
                                embed = discord.Embed(color=0xffc7ed)
                                embed.set_image(url="attachment://quote.jpg")
                                embed.set_footer(text="Powered by https://inspirobot.me/")
                                await ctx.reply(file=f, embed=embed, mention_author=True)
                            else:
                                await ctx.reply("Failed to retrieve the image from InspiroBot.", mention_author=True)
                    else:
                        await ctx.reply("Failed to generate an inspirational quote from InspiroBot.", mention_author=True)
        except aiohttp.ClientError:
            await ctx.reply("An error occurred while making the request to InspiroBot.", mention_author=True)
        except OSError:
            await ctx.reply("An error occurred while saving the image.", mention_author=True)

    @commands.command(aliases=['pngify', 'transparent'], description="Runs the provided image through a (free) API call to remove.bg, to make the image transparent.", brief="Remove the background from an image using AI")
    async def removebg(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Removing background. Please wait...", delete_after=5)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(Link_To_File) as response:
                image_data = await response.read()
                
                with open(f'{dannybot}\\cache\\removebgtemp.png', 'wb') as f:
                    f.write(image_data)
                
                headers = {
                    "X-Api-Key": os.getenv("REMOVEBG_KEY"),
                }
                
                async with session.post(
                    "https://api.remove.bg/v1.0/removebg",
                    data={"image_file": image_data, "size": "auto"},
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        result_data = await response.read()
                        
                        with open(f'{dannybot}\\cache\\removebg.png', 'wb') as f:
                            f.write(result_data)
                        
                        with open(f'{dannybot}\\cache\\removebg.png', 'rb') as f:
                            await ctx.reply(file=File(f, 'removed.png'), mention_author=True)
                    
                    else:
                        await ctx.reply("Processing of the image failed. This is most likely because no background was detected.", mention_author=True)
                        print(await response.text())

    @commands.command(description="Uses the craiyon API to send user prompts and return AI generated output.", brief="Use craiyon to create AI generated images")
    async def dalle(self, ctx, *, prompt):
        max_attempts = 3
        attempt = 0
        print("-------------------------------------")
        print(f'Dalle command ran with prompt "{prompt}"')
        
        while attempt < max_attempts:
            attempt += 1
            print(f'Attempt {attempt} for prompt "{prompt}"')
            
            try:
                images = await generate_images(prompt)
                
                if images:
                    break  # Successful generation, exit the loop
                
                print(f'Image generation failed on attempt {attempt} for prompt "{prompt}"')
            
            except Exception as e:
                print(f'Error during image generation on attempt {attempt} for prompt "{prompt}": {e}')
        
        if images:
            prompt_hyphenated = prompt.replace(" ", "-")
            collage = await make_collage(images, 3)
            b = collage
            
            try:
                print("Sending image...")
                collage_file = discord.File(collage, filename=f"{prompt_hyphenated}.{DALLE_FORMAT}")
                await ctx.reply(file=collage_file, mention_author=True)
                
                print("Caching image...")
                async with aiofiles.open(f"{dannybot}\\cache\\dalle.png", "wb") as f:
                    b.seek(0)
                    await f.write(b.read())
                
                print("Image caching successful")
            
            except Exception as e:
                print(f'Error during image handling: {e}')
        
        else:
            print(f'Image generation failed after {max_attempts} attempts for prompt "{prompt}"')
        
        print("-------------------------------------")

async def setup(bot: commands.Bot):
    await bot.add_cog(ai(bot))
# most of these are APIs

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


# Custom converter class for GPT commands
class CustomWrite(commands.FlagConverter):
    temperature: typing.Optional[float] = 1.00
    prompt: str
    top_p: typing.Optional[float] = 1.00
    frequency_penalty: typing.Optional[float] = 0.00
    presence_penalty: typing.Optional[float] = 0.00
    engine: Literal[
        "gpt-3.5-turbo-instruct-0914",
        "gpt-3.5-turbo-instruct",
        "babbage-002",
        "davinci-002",
    ]

class ai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="write",
        aliases=["davinci", "gpt"],
        description="Interact with GPT with ONLY prompts.",
        brief="Get AI generated text based on provided prompts",
    )
    async def write(self, ctx: commands.Context, *, prompt: str):
        await ctx.defer()
        try:
            gpt_prompt = str(prompt)
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=gpt_prompt,
                temperature=random.uniform(0.1, 1.0),
                max_tokens=768,
                top_p=1.0,
                frequency_penalty=0.3,
                presence_penalty=0.1,
            )
            await ctx.reply(response["choices"][0]["text"][:2000], mention_author=True)
        except Exception as e:
            await ctx.send(f"An error occurred while generating the text: **{str(e)}**")

    @commands.hybrid_command(
        name="writecustom",
        description="Interact with GPT with all the funny settings.",
        brief="Get AI generated text based on provided prompts",
    )
    async def writecustom(
        self, ctx: commands.Context, *, flags: CustomWrite, append: bool = False
    ):
        await ctx.defer()
        try:
            if append == True:
                response = openai.Completion.create(max_tokens=768, **flags.__dict__)
                await ctx.reply(
                    flags.prompt + response["choices"][0]["text"][:1600],
                    mention_author=True,
                )
            else:
                response = openai.Completion.create(max_tokens=768, **flags.__dict__)
                await ctx.reply(
                    response["choices"][0]["text"][:2000], mention_author=True
                )
        except Exception as e:
            await ctx.send(f"An error occurred while generating the text: **{str(e)}**")

    @commands.command(
        aliases=["upscale"],
        description="Locally run waifu2x using speed-optimized settings and send the results.",
        brief="Upscale images using waifu2x",
    )
    async def waifu(self, ctx, *args):
        try:
            Link_To_File = (await resolve_args(ctx, args, ctx.message.attachments))[0]
            with open(f"{dannybot}\\cache\\w2x_in.png", "wb") as f:
                f.write(requests.get(Link_To_File).content)

            os.system(
                f"{Waifu2x} -i {dannybot}\\cache\\w2x_in.png -o {dannybot}\\cache\\w2x_out.png -m noise_scale --scale_ratio 2 --noise_level 2 -x"
            )

            with open(f"{dannybot}\\cache\\w2x_out.png", "rb") as f:
                await ctx.reply(file=File(f, "waifu2x.png"))
        except Exception as e:
            await ctx.send(f"An error occurred while upscaling the image: **{str(e)}**")

    @commands.hybrid_command(
        name="inspire",
        aliases=["quote"],
        description="Sends AI generated quotes using the inspirobot API.",
        brief="Get AI generated inspirational posters",
    )
    async def inspire(self, ctx: commands.Context):
        link = "http://inspirobot.me/api?generate=true"

        try:
            async with aiohttp.ClientSession() as session, session.get(
                link
            ) as response:
                if response.status != 200:
                    raise aiohttp.ClientError(
                        "Failed to generate an inspirational quote from InspiroBot."
                    )

                file_url = await response.text()
                async with session.get(file_url) as image_response:
                    if image_response.status != 200:
                        raise aiohttp.ClientError(
                            "Failed to retrieve the image from InspiroBot."
                        )

                    image_data = await image_response.read()

            with open(f"{dannybot}\\cache\\quote.jpg", "wb") as f:
                f.write(image_data)
        except (aiohttp.ClientError, OSError) as e:
            await ctx.reply(f"An error occurred: {str(e)}", mention_author=True)
            return

        f = discord.File(f"{dannybot}\\cache\\quote.jpg", filename="quote.jpg")
        embed = discord.Embed(color=0xFFC7ED)
        embed.set_image(url="attachment://quote.jpg")
        embed.set_footer(text="Powered by https://inspirobot.me/")
        await ctx.reply(file=f, embed=embed, mention_author=True)

    @commands.command(
        aliases=["pngify", "transparent"],
        description="Runs the provided image through a (free) API call to remove.bg, to make the image transparent.",
        brief="Remove the background from an image using AI",
    )
    async def removebg(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Removing background. Please wait...", delete_after=5)

        async with aiohttp.ClientSession() as session:
            async with session.get(Link_To_File) as response:
                image_data = await response.read()

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

                        with open(f"{dannybot}\\cache\\removebg.png", "wb") as f:
                            f.write(result_data)

                        await ctx.reply(
                            file=discord.File(io.BytesIO(result_data), "removed.png"),
                            mention_author=True,
                        )

                    else:
                        await ctx.reply(
                            "Processing of the image failed. This is most likely because no background was detected.",
                            mention_author=True,
                        )
                        print(await response.text())


async def setup(bot: commands.Bot):
    await bot.add_cog(ai(bot))

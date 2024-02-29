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
        description="Runs the provided image through a rembg, to make the image transparent.",
        brief="Remove the background from an image using AI",
    )
    async def removebg(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = cmd_info[0]
        model = cmd_info[1]
        cache_dir = f"{dannybot}\\cache"

        await ctx.send(
            "Processing. Please wait...",
            delete_after=5,
        )
        image_file = f"{cache_dir}\\input.png"
        with open(image_file, "wb") as f:
            f.write(requests.get(file_url).content)

        with open(image_file, "rb") as i:
            with open(f"{cache_dir}\\output.png", "wb") as o:
                input_data = i.read()
                if model == "anime":
                    model_name = "isnet-anime"
                else:
                    model_name = "u2net"
                session = new_session(model_name)
                output_data = remove(input_data, session=session)
                o.write(output_data)

        with open(f"{cache_dir}\\output.png", "rb") as f:
            await ctx.reply(file=File(f, "transparent.png"), mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ai(bot))

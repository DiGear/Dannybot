# SHITS ABOUT TO GET REAL. - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


# Custom converter class for GPT commands
class CustomGPT(commands.FlagConverter):
    instructions: typing.Optional[str] = ""
    temperature: typing.Optional[float] = 1.00
    top_p: typing.Optional[float] = 1.00
    frequency_penalty: typing.Optional[float] = 0.00
    presence_penalty: typing.Optional[float] = 0.00
    prompt: str
    model: Literal[
        "gpt-4-turbo-preview"
        "gpt-4-1106-preview",
        "gpt-4-0613",
        "gpt-4-0314",
        "gpt-4",
        "gpt-3.5-turbo-16k-0613",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-1106"
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo",
    ]


# Class that stores every global variable and initializes them
class sentience(commands.Cog):
    def __init__(self, bot: commands.Bot, memory_length=6):
        self.bot = bot
        self.memory_length = memory_length
        self.message_array = deque([{"role": "system", "content": "Your name is Dannybot. You are talking to more than one person. Please refer to people by name as specified."}], maxlen=memory_length + 1)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.reference:
            return
        if self.bot.user.mentioned_in(message):
            async with message.channel.typing():
                content = message.content.replace(self.bot.user.mention, "").strip()
                self.message_array.append({
                    "role": "user",
                    "content": f"{message.author.display_name} said: {content}"
                })
                response_data = openai.ChatCompletion.create(
                    model="gpt-4-turbo-preview",
                    temperature=round(random.uniform(0.7, 1.5), 1),
                    messages=list(self.message_array)
                )
                response_text = response_data.choices[0].message.content.replace("Dannybot:", "").strip()[:2000]
                formatted_response = response_text.replace("fdg", "Master").replace("FDG", "Master")
                print(f"{message.author.display_name} Said: {content}")
                print(f"dannybot Said: {formatted_response}")
                await message.channel.send(formatted_response, reference=message)
                self.message_array.append({"role": "assistant", "content": formatted_response})

    @commands.hybrid_command(
        name="chatgpt",
        description="Interact with ChatGPT using instructions and prompts.",
        brief="Get AI-generated text based on provided prompts",
    )
    async def chatgpt(self, ctx: commands.Context, *, flags: CustomGPT):
        await ctx.defer()
        response = openai.ChatCompletion.create(
            model=flags.model,
            max_tokens=768,
            top_p=flags.top_p,
            temperature=flags.temperature,
            frequency_penalty=flags.frequency_penalty,
            presence_penalty=flags.presence_penalty,
            messages=[
                {"role": "system", "content": f"{flags.instructions}"},
                {"role": "user", "content": f"{flags.prompt}"},
            ],
        )
        await ctx.reply(response.choices[0].message.content[:2000], mention_author=True)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def alzheimers(self, ctx):
        self.message_array = [{"role": "system", "content": self.sysmsg}]
        self.array_index = 0

    @commands.command(hidden=True)
    @commands.is_owner()
    async def braindump(self, ctx):
        logger.debug(str(self.message_array))
        await ctx.send(str(self.message_array))


async def setup(bot: commands.Bot):
    await bot.add_cog(sentience(bot))

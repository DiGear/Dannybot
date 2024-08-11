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
        "gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4",
    ] = "gpt-4o-mini"


class chatbot(commands.Cog):
    def __init__(self, bot: commands.Bot, memory_length=5, model="gpt-4o-mini"):
        self.bot = bot
        self.memory_length = memory_length
        self.model = model
        self.message_array = deque(
            [
                {
                    "role": "system",
                    "content": """
            Your name is Dannybot. You are talking to more than one person. The name format is (name said: thing) respond to their message
            """,
                }
            ],
            maxlen=memory_length + 1,
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author.bot
            or message.reference
            or message.guild.id not in whitelist
            or not self.bot.user.mentioned_in(message)
        ):
            return

        content = [
            {
                "type": "text",
                "text": f"{message.author.display_name} said: {message.content}",
            }
        ]

        if message.attachments:
            attachment_url = message.attachments[0].url
            content.append(
                {"type": "image_url", "image_url": {"url": str(attachment_url)}}
            )

        self.message_array.append({"role": "user", "content": content})

        if len(self.message_array) > self.memory_length:
            self.pop_not_sys()

        response_text = await self.get_openai_response()
        response_text = self.clean_response(response_text)
        await message.channel.send(response_text, reference=message)
        self.message_array.append({"role": "assistant", "content": response_text})
        print(self.message_array)

    async def get_openai_response(self) -> str:
        response_data = openai.ChatCompletion.create(
            model=self.model,
            temperature=1.0,
            max_tokens=750,
            messages=list(self.message_array),
        )
        return response_data.choices[0].message.content

    def clean_response(self, response_text: str) -> str:
        response_text = re.sub(r"(?i)dannybot:", "", response_text)
        response_text = re.sub(r"(?i)dannybot said:", "", response_text).strip()[:1990]
        return response_text

    def pop_not_sys(self):
        for msg in list(self.message_array):
            if msg["role"] != "system":
                self.message_array.remove(msg)
                break

    @commands.hybrid_command(
        name="chatgpt",
        description="Interact with ChatGPT using instructions and prompts.",
        brief="Get AI-generated text based on provided prompts",
    )
    async def chatgpt(self, ctx: commands.Context, *, flags: CustomGPT):
        await ctx.defer()
        if ctx.guild.id not in whitelist:
            await ctx.send("This server is not whitelisted for this command.")
            return
        response = openai.ChatCompletion.create(
            model=flags.model,
            max_tokens=750,
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


async def setup(bot: commands.Bot):
    await bot.add_cog(chatbot(bot))
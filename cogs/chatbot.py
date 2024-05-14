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
        "gpt-4o",
        "gpt-4-turbo-preview",
        "gpt-4",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo"
    ]

# Class that stores every global variable and initializes them
class chatbot(commands.Cog):
    def __init__(self, bot: commands.Bot, memory_length=12):
        self.bot = bot
        self.memory_length = memory_length
        self.message_array = deque([{"role": "system", "content": '''
            Your name is Dannybot. You are talking to more than one person. Please refer to people by name as specified (The name will be displayed as "name said:").
            '''}], maxlen=memory_length + 1)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.reference:
            return
        
        if message.guild.id not in whitelist:
            return

        if self.bot.user.mentioned_in(message):
            content = [{"type": "text", "text": f"{message.author.display_name} said: {message.content}"}]
            
            if message.attachments:
                attachment_url = message.attachments[0].url
                content.append({"type": "image_url", "image_url": {"url": str(attachment_url)}})
            
            self.message_array.append({"role": "user", "content": content})
            
            if len(self.message_array) > self.memory_length:
                self.remove_image_messages()
                self.pop_not_sys()
            
            print(self.message_array)

            model = "gpt-4o" if message.attachments else "gpt-3.5-turbo"
            response_data = openai.ChatCompletion.create(
                model=model,
                temperature=1,
                messages=list(self.message_array)
            )
            response_text = response_data.choices[0].message.content
            response_text = re.sub(r'(?i)dannybot:', '', response_text)
            response_text = re.sub(r'(?i)dannybot said:', '', response_text).strip()[:1990]

            await message.channel.send(response_text, reference=message)
            self.message_array.append({"role": "assistant", "content": response_text})
        
        def pop_not_sys(self):
            for msg in reversed(self.message_array):
                if msg["role"] != "system":
                    self.message_array.remove(msg)
                    break
        
        def remove_image_messages(self):
            new_message_array = []
            for msg in reversed(self.message_array):
                if not any(content.get("image_url") for content in msg["content"]):
                    new_message_array.append(msg)
            self.message_array = new_message_array


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
            max_tokens=512,
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

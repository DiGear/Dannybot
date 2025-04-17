from config import *


# custom FlagConverter class for GPT command arguments
class CustomGPT(commands.FlagConverter):
    """
    this is a FlagConverter parses flags for the ChatGPT command.
    parameters:
        - instructions (str): additional system instructions for the AI.
        - temperature (float): controls temperature idk how to describe this. keep it between 0.5 and 2 for the most part.
        - top_p (float): controls reponse diversity.
        - frequency_penalty (float): reduces repetition.
        - presence_penalty (float): increases chance of unique word choice??.
        - prompt (str): user input for the GPT model.
        - model (str): the model selection".
    """

    instructions: typing.Optional[str] = ""
    temperature: typing.Optional[float] = 1.00
    top_p: typing.Optional[float] = 1.00
    frequency_penalty: typing.Optional[float] = 0.00
    presence_penalty: typing.Optional[float] = 0.00
    prompt: str
    model: Literal[
        "gpt-4.1-nano"
        "gpt-4.1-mini",
        "gpt-4o-mini",
        "gpt-pizzi",
        "o4-mini",
        "o3-mini",
        "o1-mini",
    ] = "gpt-4.1-nano"


# class for the cog where i store most of the script-wide variables
class chatbot(commands.Cog):
    def __init__(self, bot: commands.Bot, memory_length=6, model="gpt-4.1-nano"):
        self.bot = bot
        self.memory_length = memory_length  # length of conversation history
        self.model = model

        # the system message influences how GPT responds
        self.system_message = {
            "role": "system",
            "content": (
                "Your name is Dannybot, a Discord bot that responds to people in a chatroom. "
                "Also, you are typically talking to more than one person. "
                "The name format is USERNAME said: CONTENT, respond to their messages."
            ),
        }

        # we store the conversation history here
        self.conversation_history = deque(maxlen=memory_length)

        # the parameters for GPT
        self.temperature = 1.2
        self.top_p = 1.0
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0

        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author.bot  # ignore bots
            or message.guild.id not in whitelist  # check if server is whitelisted
            or not self.bot.user.mentioned_in(message)  # only respond if mentioned
            or any(
                message.content.startswith(prefix) for prefix in dannybot_prefixes
            )  # don't respond to anything command related
        ):
            return

        # more command ignorance shit
        if message.reference and (
            "d." in message.content.lower()
            or "#" in message.content.lower()
            or "ratio +" in message.content.lower()
        ):
            return

        # format the message content
        content = [
            {
                "type": "text",
                "text": f"{message.author.display_name} said: {message.content}",
            }
        ]

        # if there any any attachments we put the first one in the content we send to GPT
        if message.reference:
            referenced_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            if referenced_message.attachments:
                attachment_url = referenced_message.attachments[0].url
                content.append(
                    {"type": "image_url", "image_url": {"url": str(attachment_url)}}
                )

        # the same thing as above but for not replies
        if message.attachments:
            attachment_url = message.attachments[0].url
            content.append(
                {"type": "image_url", "image_url": {"url": str(attachment_url)}}
            )

        # update the conversation history
        self.conversation_history.append({"role": "user", "content": content})

        try:
            response_text = await self.get_openai_response()
            response_text = self.clean_response(response_text)
            await message.channel.send(response_text, reference=message)

            # update the conversation history again
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )
        except Exception as e:
            self.logger.exception("an error occurred: %s\nreloading the cog...", e)
            self.bot.reload_extension("chatbot")

    async def get_openai_response(self) -> str:

        # add the system message to the conversation history
        messages = [self.system_message] + list(self.conversation_history)

        # we prepare a separate thread for the call to OpenAI incase it takes a while
        loop = asyncio.get_running_loop()
        try:
            response_data = await loop.run_in_executor(
                None,
                # lamba function that calls the API and passes in our parameters
                lambda: openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    max_tokens=750,
                    messages=messages,
                ),
            )
            return response_data.choices[0].message.content
        except Exception as ex:
            self.logger.exception("%s", ex)
            raise

    def clean_response(self, response_text: str) -> str:
        """cleans up GPTs response by removing potential bot mentions and name formats."""
        response_text = re.sub(r"(?i)dannybot:", "", response_text)
        response_text = re.sub(r"(?i)dannybot-s:", "", response_text)
        response_text = re.sub(r"(?i)\b.+?\b said:", "", response_text).strip()[
            :1990
        ]  # this is a little bit below the 2000 character limit but i like to be safe
        return response_text

    # i cant be fucked to comment this and its basically the same thing as the one above anyways
    @commands.hybrid_command(
        name="chatgpt",
        description="Interact with ChatGPT using instructions and prompts.",
    )
    async def chatgpt(self, ctx: commands.Context, *, flags: CustomGPT):
        await ctx.defer()
        if (
            ctx.guild is not None and ctx.guild.id not in whitelist
        ) and ctx.author.id != 343224184110841856:
            await ctx.send("This server is not whitelisted for this command.")
            return

        if (
            flags.model == "gpt-pizzi"
        ):  # this is an override for the pizzi model that also passes shit into the system message
            modelname = (
                "ft:gpt-4o-mini-2024-07-18:personal:pizzi:9v9U1nDc:ckpt-step-1464"
            )
            nuinstructions = "you are pizzi." + flags.instructions
        else:
            modelname = flags.model
            nuinstructions = flags.instructions

        messages = [
            {"role": "system", "content": nuinstructions.replace("/n", "\n")},
            {"role": "user", "content": flags.prompt.replace("/n", "\n")},
        ]
        response = openai.ChatCompletion.create(
            model=modelname, max_tokens=750, messages=messages
        )
        await ctx.reply(response.choices[0].message.content[:2000], mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(chatbot(bot))

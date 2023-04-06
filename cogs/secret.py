# huh

# if you can't find a variable used in this file its probably imported from here
from config import *


class secret(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #bookmark feature
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, bookmark):
        if bookmark.member.id == 343224184110841856:
                if str(bookmark.emoji)[0] =='🔖':
                    reaction = '✅' #reaction to add to message
                    MessageChannel=self.bot.get_channel(bookmark.channel_id) #set channel to message's channel
                    input=await MessageChannel.fetch_message(bookmark.message_id)
                    message_link = input.jump_url
                    await self.bot.get_channel(bookmarks_channel).send(f'{message_link}') #send a message to the logs channel
                    await input.add_reaction(reaction) #add a reaction to the message
        else:
            return
        
    @commands.command(hidden=True)
    async def taur_add(self, ctx, file_url: typing.Optional[str] = "File_Is_Attachment"):
        if not ctx.author.id in [206392667351941121, 343224184110841856]: # hardcoded whitelist lol lmao
            await ctx.send("You are not whitelisted for this command!")
            return
        else:
            if(file_url == "File_Is_Attachment"):
                link_to_file = ctx.message.attachments[0].url
            else:
                link_to_file = file_url
            await ctx.send("Downloading...", delete_after=5)


            # this code block writes the image data to a file
            with open(f"{dannybot}\\database\\Taurs\\{randhex(64)}.png", 'wb') as f:
                f.write(requests.get(link_to_file).content)
                f.close
            await ctx.send("File Downloaded!", delete_after=5)

    @commands.command(hidden=True)
    async def taur(self, ctx):
        dir = f"{dannybot}\\database\\Taurs"
        file_name = random.choice(os.listdir(dir))

        with open(f'{dir}\\{file_name}', 'rb') as f:
            await ctx.reply(file=File(f, 'Taur.png'), mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(secret(bot))
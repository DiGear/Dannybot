# this is most likely gonna be necessary for expanding upon pooter later

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        if any(input.content.startswith(prefix + "poo") for prefix in dannybot_prefixes):
            poopoo = input.content.count("poo")
            if poopoo > 1:
                for poo in range(0, poopoo):
                    pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
                    with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                        picture = discord.File(f)
                        await input.channel.send(file=picture, reference=input)
                        f.close
                    poo - 1

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        #bookmark code
        if payload.member.id == 343224184110841856 and str(payload.emoji)[0] == '🔖':
            message_channel = self.bot.get_channel(payload.channel_id)  # Set the channel to the message's channel
            input_message = await message_channel.fetch_message(payload.message_id)
            message_link = input_message.jump_url
            await self.bot.get_channel(bookmarks_channel).send(message_link)  # Send the message link to the bookmarks channel

        
        #pooter code
        if str(payload.emoji)[0] == '💩':  # Check if the emoji is poop
            message_channel = self.bot.get_channel(payload.channel_id)  # Get the channel of the message
            input_message = await message_channel.fetch_message(payload.message_id)  # Fetch the actual message from the channel

            downloads = 1  # Downloads counter
            reaction = '✅'  # Reaction to add to the message
            f_name = randhex(128)  # Random hex name for the file

            if input_message.attachments:  # If there are attachments
                for attachment in input_message.attachments:  # Iterate over each attachment
                    if not any(ext in attachment.url for ext in database_acceptedFiles):
                        await message_channel.send('This file is not a valid image or video file!')
                        return

                    link_to_file = attachment.url  # Get the URL of the attachment
                    await message_channel.send(f'Downloading... {downloads} of {len(input_message.attachments)}', delete_after=1)  # Send a message indicating the number of downloads
                    downloads += 1  # Increment the downloads counter

                    sanitized_link = link_to_file.replace("/", '')
                    with open(f'{dannybot}\\database\\Pooter\\{f_name}{sanitized_link[-6:]}', 'wb') as file:
                        file.write(requests.get(link_to_file).content)  # Write the file content to the file
                        file.close()  # Close the file

                    await self.bot.get_channel(logs_channel).send(f'{payload.member.name}: {payload.member.id} has pootered {link_to_file}')  # Send a message to the logs channel

                await input_message.add_reaction(reaction)  # Add a reaction to the message
            else:  # If there is a URL in the message
                link_to_file = input_message.content.strip()
                if not any(ext in link_to_file for ext in database_acceptedFiles):
                    await message_channel.send('This file is not a valid image or video file!')
                    return

                await message_channel.send('Downloading... (1 of 1)', delete_after=1)  # Send a message indicating the number of downloads

                sanitized_link = link_to_file.replace("/", '')
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{sanitized_link[-6:]}', 'wb') as file:
                    file.write(requests.get(link_to_file).content)  # Write the file content to the file
                    file.close()  # Close the file

                await self.bot.get_channel(logs_channel).send(f'{payload.member.name}: {payload.member.id} has pootered {link_to_file}')  # Send a message to the logs channel

                await input_message.add_reaction(reaction)  # Add a reaction to the message

    @commands.command(aliases=["poo", "poop"], description="Send or receive a file from a user-built archive of files. You can upload 10 files at a time, or not attach any files to view the archive instead.", brief="Send/Receive files from a public archive.")
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        downloads = 1  # Downloads counter
        reaction = '✅'  # Reaction to add to the message
        f_name = randhex(128)  # Random hex name for the file

        if ctx.message.attachments:
            for i, attachment in enumerate(ctx.message.attachments, start=1):
                if not any(ext in attachment.url for ext in database_acceptedFiles):
                    await ctx.send('This file is not a valid image or video file!')
                    return

                await ctx.send(f'Downloading... {downloads} of {len(ctx.message.attachments)}', delete_after=1)
                downloads += 1
                sanitized_link = attachment.url.replace("/", '')
                with open(f'{dannybot}/database/Pooter/{f_name}{sanitized_link[-6:]}', 'wb') as f:
                    f.write(requests.get(attachment.url).content)

                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {attachment.url}')

            await ctx.message.add_reaction(reaction)
        elif not File_Url:
            pooter_files = os.listdir(f'{dannybot}/database/Pooter/')
            pooter_file = random.choice(pooter_files)
            with open(f'{dannybot}/database/Pooter/{pooter_file}', 'rb') as f:
                await ctx.reply(file=discord.File(f, pooter_file))
        else:
            if not any(ext in File_Url for ext in database_acceptedFiles):
                await ctx.send('This file is not a valid image or video file!')
                return

            await ctx.send("Downloading... (1 of 1)", delete_after=1)
            sanitized_link = File_Url.replace("/", '')
            with open(f'{dannybot}/database/Pooter/{f_name}{sanitized_link[-6:]}', 'wb') as f:
                f.write(requests.get(File_Url).content)

            await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {File_Url}')
            await ctx.message.add_reaction(reaction)

async def setup(bot: commands.Bot):
    await bot.add_cog(pooter(bot))

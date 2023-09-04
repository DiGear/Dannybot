# this is most likely gonna be necessary for expanding upon pooter later

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class pooter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if (msg.guild.id == 1089076875999072296 or 
            not any(msg.content.startswith(f"{pfx}poo") for pfx in dannybot_prefixes)):
            return
        
        poo_count = msg.content.count("poo")
        pooter_db_path = os.path.join(dannybot, "database", "Pooter")\
        
        if poo_count == 1:
            return

        for _ in range(poo_count):
            img_file = random.choice(os.listdir(pooter_db_path))
            with open(os.path.join(pooter_db_path, img_file), 'rb') as img:
                await msg.channel.send(file=discord.File(img), reference=msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id == 343224184110841856 and str(payload.emoji)[0] == '🔖':
            message_channel = self.bot.get_channel(payload.channel_id)
            input_message = await message_channel.fetch_message(payload.message_id)     
            message_link = input_message.jump_url
            await self.bot.get_channel(bookmarks_channel).send(message_link)

        if str(payload.emoji)[0] == '💩':
            message_channel = self.bot.get_channel(payload.channel_id)
            input_message = await message_channel.fetch_message(payload.message_id)
            
            downloads = 1
            reaction = '✅'
            f_name = randhex(128)
            
            async def download_file(attachment_url, download_count):
                # Check if the attachment URL is a valid image or video file
                if not any(ext in attachment_url.lower() for ext in database_acceptedFiles):
                    await message_channel.send('This file is not a valid image or video file!')
                    return
                await message_channel.send(f'Downloading... {download_count} of {len(input_message.attachments)}', delete_after=1)
                
                # Sanitize the attachment URL to use it as part of the file name
                sanitized_link = attachment_url.replace("/", '')
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{sanitized_link[-6:]}', 'wb') as file:
                    file.write(requests.get(attachment_url).content)

                await self.bot.get_channel(logs_channel).send(f'{payload.member.global_name} ({payload.member.id}) has pootered: {attachment_url}')

            # Check if the message has attachments
            if input_message.attachments:
                for download_count, attachment in enumerate(input_message.attachments, 1):
                    await download_file(attachment.url, download_count)
            else:
                # If there are no attachments, assume the message contains a link to a file
                link_to_file = input_message.content.strip()
                total_downloads = 1  # Initialize total_downloads to 1 for links
                await download_file(link_to_file, 1)

            await input_message.add_reaction(reaction)

    @commands.command(hidden=True, aliases=["poo", "poop", ":spoon:", "🥄"], description="Send or receive a file from a user-built archive of files. You can upload 10 files at a time, or not attach any files to view the archive instead.", brief="Send/Receive files from a public archive.")
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        if ctx.guild.id == 1089076875999072296:
            return

        async def download_file(url):
            nonlocal downloads
            nonlocal reaction

            if not any(ext in url for ext in database_acceptedFiles):
                await ctx.send('This file is not a valid image or video file!')
                return

            await ctx.send(f'Downloading... {downloads} of {total_downloads}', delete_after=1)
            downloads += 1
            sanitized_link = url.replace("/", '')
            with open(f'{dannybot}/database/Pooter/{f_name}{sanitized_link[-6:]}', 'wb') as f:
                f.write(requests.get(url).content)

            await self.bot.get_channel(logs_channel).send(f'{ctx.author.global_name} ({ctx.author.id}) has pootered: {url}')

        downloads = 1
        reaction = '✅'
        f_name = randhex(128)

        total_downloads = 0  # Initialize total_downloads here

        if ctx.message.attachments:
            total_downloads = len(ctx.message.attachments)
            for attachment in ctx.message.attachments:
                await download_file(attachment.url)
            await ctx.message.add_reaction(reaction)
        elif not File_Url:
            pooter_files = os.listdir(f'{dannybot}/database/Pooter/')
            pooter_file = random.choice(pooter_files)
            with open(f'{dannybot}/database/Pooter/{pooter_file}', 'rb') as f:
                await ctx.reply(file=discord.File(f, pooter_file))
        else:
            total_downloads = 1  # Initialize total_downloads to 1 for links
            await download_file(File_Url)
            await ctx.message.add_reaction(reaction)

async def setup(bot: commands.Bot):
    await bot.add_cog(pooter(bot))

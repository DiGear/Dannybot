# this is most likely gonna be necessary for expanding upon pooter later

# if you can't find a variable used in this file its probably imported from here
from config import *

class booru(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, input: discord.Message):
        if any(input.content.startswith(prefix) for prefix in dannybot_prefixes):
            poopoo = -1
            for i in input.content.split("poo"):
                    poopoo += 1
            if poopoo > 1:
                for poo in range(0, poopoo):
                    pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\'))
                    with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f:
                        picture = discord.File(f)
                        await input.channel.send(file=picture, reference=input)
                        f.close
                    poo - 1

    @commands.command(aliases=["poo"], description="Send or recieve a file from a user-built archive of files. You can upload 10 files at a time, or not attach any files to view the archive instead.", brief="Send/Recieve files from a public archive.") #command description
    async def pooter(self, ctx, File_Url: typing.Optional[str] = None):
        downloads = 1 #downloads counter
        reaction = '✅' #reaction to add to message
        f_name = randhex(128) #random hex name for file
        if ctx.message.attachments: #if there are attachments
            for i in ctx.message.attachments: #for each attachment
                Link_To_File = i.url #get the url
                await ctx.send(f'Downloading... {downloads} of {len(ctx.message.attachments)}', delete_after=1) #send a message saying how many downloads there are
                downloads += 1 #add 1 to the downloads counter
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f: #open a file with the random hex name and the file extension
                    f.write(requests.get(Link_To_File).content) #write the file to the file
                    f.close #close the file
                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {Link_To_File}') #send a message to the logs channel
            await ctx.message.add_reaction(reaction) #add a reaction to the message
        elif File_Url == None: #if there is no url
            pooter_file = random.choice(os.listdir(f'{dannybot}\\database\\Pooter\\')) #choose a random file from the pooter folder
            with open(f'{dannybot}\\database\\Pooter\\{pooter_file}', 'rb') as f: #open the file
                await ctx.reply(file=File(f, pooter_file)) #send the file
        else: #if there is a url
                Link_To_File = File_Url #get the url
                await ctx.send("Downloading... (1 of 1)", delete_after=1) #send a message saying how many downloads there are
                with open(f'{dannybot}\\database\\Pooter\\{f_name}{Link_To_File[-4:]}', 'wb') as f: #open a file with the random hex name and the file extension
                    f.write(requests.get(Link_To_File).content) #write the file to the file
                    f.close #close the file
                await self.bot.get_channel(logs_channel).send(f'{ctx.author.name}: {ctx.author.id} has pootered {Link_To_File}') #send a message to the logs channel
                await ctx.message.add_reaction(reaction) #add a reaction to the message

async def setup(bot: commands.Bot):
    await bot.add_cog(booru(bot))

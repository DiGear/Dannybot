# this is where the shit hits the fan, pretty much - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *

class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Flips a provided image vertically.", brief="Flips an image vertically")
    async def flip(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\flip.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    im = PIL.Image.open(f"{dannybot}\\cache\\ffmpeg\\{frame}")
                    im_mirror = ImageOps.flip(im)
                    im_mirror.save(f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            im = PIL.Image.open(f'{dannybot}\\cache\\flip.png')
            im_mirror = ImageOps.flip(im)
            im_mirror.save(f'{dannybot}\\cache\\flipped.png')
            file_name = f"{dannybot}\\cache\\flipped.png"
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.png'), mention_author=True)
                f.close

    @commands.command(description="Flips a provided image horizontally.", brief="Flips an image horizontally")
    async def mirror(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\mirror.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    im = PIL.Image.open(f"{dannybot}\\cache\\ffmpeg\\{frame}")
                    im_mirror = ImageOps.mirror(im)
                    im_mirror.save(f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            im = PIL.Image.open(f'{dannybot}\\cache\\mirror.png')
            im_mirror = ImageOps.mirror(im)
            im_mirror.save(f'{dannybot}\\cache\\mirrored.png')
            file_name = f"{dannybot}\\cache\\mirrored.png"
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.png'), mention_author=True)
                f.close

    @commands.command(aliases=['petthe', 'pet-the', 'pet_the'], description="Applies a petting hand gif to the provided image.", brief="That funny hand-petting gif that was a popular meme for a bit")
    async def pet(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        with open(f'{dannybot}\\cache\\pet_in.png', 'wb') as f:
            f.write(requests.get(Link_To_File).content)
            f.close
        petpet.make(f'{dannybot}\\cache\\pet_in.png', f'{dannybot}\\cache\\pet_out.gif')
        with open(f'{dannybot}\\cache\\pet_out.gif', 'rb') as f:
            await ctx.reply(file=File(f, 'pet_the.gif')) 
            f.close
            
    @commands.command(aliases=['distort', 'magic'], description="Applies a liquid rescale effect to the provided image, using the provided value.", brief="Recreation of NotSoBots 'magik' command")
    async def magik(self, ctx, *args):
        context = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = context[0]
    
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\magik_in.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    imagebounds(frame)
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        img.liquid_rescale(width=int(img.width * 0.5), height=int(img.height * 0.5), delta_x=1, rigidity=0)
                        img.liquid_rescale(width=int(img.width * 2), height=int(img.height * 2), delta_x=2, rigidity=0)
                        img.save(filename=f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'magik.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
                return
        else:
            imagebounds(f'{dannybot}\\cache\\magik_in.png')
            with magick(filename=f'{dannybot}\\cache\\magik_in.png') as img:
                img.liquid_rescale(width=int(img.width * 0.5), height=int(img.height * 0.5), delta_x=1, rigidity=0)
                img.liquid_rescale(width=int(img.width * 2), height=int(img.height * 2), delta_x=2, rigidity=0)
                img.save(filename=f'{dannybot}\\cache\\magik_out.png')
            with open(f'{dannybot}\\cache\\magik_out.png', 'rb') as f:
                await ctx.reply(file=File(f, 'magik.png'), mention_author=True)
                f.close
                return
                
    @commands.command(aliases=['df'], description="'Deepfries' the provided image.", brief="'Deepfries' an image")
    async def deepfry(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\deepfry_in.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    deepfry(f"{dannybot}\\cache\\ffmpeg\\{frame}", f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'deepfried.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            deepfry(f'{dannybot}\\cache\\deepfry_in.png', f'{dannybot}\\cache\\deepfry_out.png')
            file_name = f'{dannybot}\\cache\\deepfry_out.png'
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'deepfried.png'), mention_author=True)
                f.close

    @commands.command(description="Turns a provided image into a low quality jpeg.", brief="Turns an image into a low quality jpeg")
    async def shittify(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\jpg_in.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\{frame}').convert('RGB')
                    image.save(f"{dannybot}\\cache\\ffmpeg\\output\\{frame}.jpg", quality=15)
            repack_gif_JPG()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'jpg-ed.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            image = PIL.Image.open(f'{dannybot}\\cache\\jpg_in.png').convert('RGB')
            image.save(f'{dannybot}\\cache\\jpg_out.jpg', quality=15)
            file_name = f'{dannybot}\\cache\\jpg_out.jpg'
            with open(f'{file_name}', 'rb') as f:
                await ctx.reply(file=File(f, 'jpg-ed.jpg'), mention_author=True)
                f.close

    @commands.command(aliases=['oatmeal'], description="Makes an image super pixelated. The name(s) of the command are in reference to Vinesauce Joel.", brief="Makes an image super pixelated")
    async def koala(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:
            with open(f'{dannybot}\\cache\\koala_in.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\{frame}')
                    koala1 = image.resize((round(image.size[0]*0.07), round(image.size[1]*0.07)), PIL.Image.Resampling.NEAREST)
                    koala1.save(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
                    koala2 = image.resize((round(image.size[0]*9.6835), round(image.size[1]*9.72)), PIL.Image.Resampling.NEAREST)
                    koala2.save(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            image = PIL.Image.open(f'{dannybot}\\cache\\koala_in.png')
            koala1 = image.resize((round(image.size[0]*0.07), round(image.size[1]*0.07)), PIL.Image.Resampling.NEAREST)
            koala1.save(f'{dannybot}\\cache\\koala_small.png')
            image = PIL.Image.open(f'{dannybot}\\cache\\koala_small.png')
            koala2 = image.resize((round(image.size[0]*9.6835), round(image.size[1]*9.72)), PIL.Image.Resampling.NEAREST)
            koala2.save(f'{dannybot}\\cache\\koala_out.png')
            with open(f'{dannybot}\\cache\\koala_out.png', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.png'), mention_author=True)
                f.close

    # i have a feeling im making this more complicated than it needs to be - FDG
    @commands.command(description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext", brief="Turns an image into an impact font meme")
    async def meme(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        
        # distinquish between command arguments and command file uploads
        context = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = context[0]
        meme_text = context[1]
        
        # gif files suck! - FDG
        if '.gif' in file_url or 'https://tenor.com/' in file_url:
            is_gif = True
        else:
            is_gif = False
        
        # this downloads the image to be meme'd and then configures all of the args appropriately
        with open(f"{dannybot}\\cache\\meme_in.png", 'wb') as f:
                    f.write(requests.get(file_url).content)
                    f.close
        png_path = (f"{dannybot}\\cache\\meme_in.png")

        # split the meme text by top and bottom and then capitalize it
        if ("|" in meme_text):
            meme_text_splitted = meme_text.split("|")
            Top_Text = meme_text_splitted[0].upper()
            Bottom_Text = meme_text_splitted[1].upper()
        else:
            Top_Text = meme_text.upper()
            Bottom_Text = ""

        # determine if we need to call the standard function or gif function
        if (is_gif):
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(file_url).content)
                f.close
            unpack_gif(f"{dannybot}\\cache\\gif.gif")
            make_meme_gif(Top_Text, Bottom_Text)
            repack_gif()
        else:
            make_meme(Top_Text, Bottom_Text, png_path)

        # determine if we need to send a gif or png in response
        if (is_gif):
            with open(f"{dannybot}\\cache\\ffmpeg_out.gif", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:
            with open(f"{dannybot}\\cache\\meme_out.png", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.png'), mention_author=True)
                f.close

async def setup(bot: commands.Bot):
    await bot.add_cog(image(bot))
# this is where the shit hits the fan, pretty much - FDG

# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Flips a provided image vertically.", brief="Flips an image vertically")
    async def flip(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = cmd_info[0]
        cache_dir = f'{dannybot}\\cache'

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in file_url:
            gif_file = f'{cache_dir}\\gif.gif'
            with open(gif_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(gif_file)

            for frame in os.listdir(f'{cache_dir}\\ffmpeg'):
                if '.png' in frame:
                    im = PIL.Image.open(f"{cache_dir}\\ffmpeg\\{frame}")
                    im_flip = ImageOps.flip(im)
                    im_flip.save(f"{cache_dir}\\ffmpeg\\output\\{frame}")

            repack_gif()

            with open(f'{cache_dir}\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            image_file = f'{cache_dir}\\flip.png'
            with open(image_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            im = PIL.Image.open(image_file)
            im_flip = ImageOps.flip(im)
            flipped_file = f'{cache_dir}\\flipped.png'
            im_flip.save(flipped_file)

            with open(flipped_file, 'rb') as f:
                await ctx.reply(file=File(f, 'flipped.png'), mention_author=True)

    @commands.command(description="Flips a provided image horizontally.", brief="Flips an image horizontally")
    async def mirror(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = cmd_info[0]
        cache_dir = f'{dannybot}\\cache'

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in file_url:
            gif_file = f'{cache_dir}\\gif.gif'
            with open(gif_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(gif_file)

            for frame in os.listdir(f'{cache_dir}\\ffmpeg'):
                if '.png' in frame:
                    im = PIL.Image.open(f"{cache_dir}\\ffmpeg\\{frame}")
                    im_mirror = ImageOps.mirror(im)
                    im_mirror.save(f"{cache_dir}\\ffmpeg\\output\\{frame}")

            repack_gif()

            with open(f'{cache_dir}\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            image_file = f'{cache_dir}\\mirror.png'
            with open(image_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            im = PIL.Image.open(image_file)
            im_mirror = ImageOps.mirror(im)
            mirrored_file = f'{cache_dir}\\mirrored.png'
            im_mirror.save(mirrored_file)

            with open(mirrored_file, 'rb') as f:
                await ctx.reply(file=File(f, 'mirrored.png'), mention_author=True)

    @commands.command(aliases=['petthe', 'pet-the', 'pet_the'], description="Applies a petting hand gif to the provided image.", brief="That funny hand-petting gif that was a popular meme for a bit")
    async def pet(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        link_to_file = cmd_info[0]
        cache_dir = f'{dannybot}\\cache'

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        image_file = f'{cache_dir}\\pet_in.png'
        with open(image_file, 'wb') as f:
            f.write(requests.get(link_to_file).content)

        petpet.make(image_file, f'{cache_dir}\\pet_out.gif')

        with open(f'{cache_dir}\\pet_out.gif', 'rb') as f:
            await ctx.reply(file=File(f, 'pet_the.gif'))
            
    @commands.command(aliases=['distort', 'magic'], description="Applies a liquid rescale effect to the provided image.", brief="Recreation of NotSoBots 'magik' command")
    async def magik(self, ctx, *args):
        context = await resolve_args(ctx, args, ctx.message.attachments)
        file_url = context[0]
        is_gif = '.gif' in file_url
        cache_dir = f'{dannybot}\\cache'
        output_dir = f'{cache_dir}\\output'
        output_file = 'magik.gif' if is_gif else 'magik.png'

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if is_gif:
            gif_file = f'{cache_dir}\\gif.gif'
            with open(gif_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(gif_file)

            for frame in os.listdir(f'{cache_dir}\\ffmpeg'):
                if '.png' in frame:
                    imagebounds(f"{cache_dir}\\ffmpeg\\{frame}")
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        img.liquid_rescale(width=int(img.width * 0.5), height=int(img.height * 0.5), delta_x=1, rigidity=0)
                        img.liquid_rescale(width=int(img.width * 2), height=int(img.height * 2), delta_x=2, rigidity=0)
                        img.save(filename=f"{output_dir}\\{frame}")

            repack_gif()

            with open(f'{cache_dir}\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, output_file), mention_author=True)
                cleanup_ffmpeg()
        else:
            image_file = f'{cache_dir}\\magik_in.png'
            with open(image_file, 'wb') as f:
                f.write(requests.get(file_url).content)

            imagebounds(image_file)
            with magick(filename=f'{dannybot}\\cache\\magik_in.png') as img:
                img.liquid_rescale(width=int(img.width * 0.5), height=int(img.height * 0.5), delta_x=1, rigidity=0)
                img.liquid_rescale(width=int(img.width * 2), height=int(img.height * 2), delta_x=2, rigidity=0)
                img.save(filename=f'{cache_dir}\\magik_out.png')

            with open(f'{cache_dir}\\magik_out.png', 'rb') as f:
                await ctx.reply(file=File(f, output_file), mention_author=True)
                    
    @commands.command(aliases=['df'], description="'Deepfries' the provided image.", brief="'Deepfries' an image")
    async def deepfry(self, ctx, *args):
        file_url, _ = await resolve_args(ctx, args, ctx.message.attachments)
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in file_url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    deepfry(f"{dannybot}\\cache\\ffmpeg\\{frame}", f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'deepfried.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            
            with open(f'{dannybot}\\cache\\deepfry_in.png', 'wb') as f:
                f.write(requests.get(file_url).content)
            
            deepfry(f'{dannybot}\\cache\\deepfry_in.png', f'{dannybot}\\cache\\deepfry_out.png')
            file_name = f'{dannybot}\\cache\\deepfry_out.png'

            with open(file_name, 'rb') as f:
                await ctx.reply(file=File(f, 'deepfried.png'), mention_author=True)

    @commands.command(description="Turns a provided image into a low quality jpeg.", brief="Turns an image into a low quality jpeg")
    async def shittify(self, ctx, *args):
        file_url, _ = await resolve_args(ctx, args, ctx.message.attachments)
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in file_url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\{frame}').convert('RGB')
                    image.save(f"{dannybot}\\cache\\ffmpeg\\output\\{frame}.jpg", quality=15)
            repack_gif_JPG()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'jpg-ed.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            image = PIL.Image.open(requests.get(file_url, stream=True).raw).convert('RGB')
            image.save(f'{dannybot}\\cache\\jpg_out.jpg', quality=15)

            with open(f'{dannybot}\\cache\\jpg_out.jpg', 'rb') as f:
                await ctx.reply(file=File(f, 'jpg-ed.jpg'), mention_author=True)

    @commands.command(aliases=['oatmeal'], description="Makes an image super pixelated. The name(s) of the command are in reference to Vinesauce Joel.", brief="Makes an image super pixelated")
    async def koala(self, ctx, *args):
        file_url, _ = await resolve_args(ctx, args, ctx.message.attachments)
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in file_url:
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\{frame}')
                    koala1 = image.resize((round(image.size[0] * 0.07), round(image.size[1] * 0.07)), PIL.Image.Resampling.NEAREST)
                    koala1.save(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
                    image = PIL.Image.open(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
                    koala2 = image.resize((round(image.size[0] * 9.6835), round(image.size[1] * 9.72)), PIL.Image.Resampling.NEAREST)
                    koala2.save(f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            image = PIL.Image.open(requests.get(file_url, stream=True).raw)
            koala1 = image.resize((round(image.size[0] * 0.07), round(image.size[1] * 0.07)), PIL.Image.Resampling.NEAREST)
            koala1.save(f'{dannybot}\\cache\\koala_small.png')
            image = PIL.Image.open(f'{dannybot}\\cache\\koala_small.png')
            koala2 = image.resize((round(image.size[0] * 9.6835), round(image.size[1] * 9.72)), PIL.Image.Resampling.NEAREST)
            koala2.save(f'{dannybot}\\cache\\koala_out.png')

            with open(f'{dannybot}\\cache\\koala_out.png', 'rb') as f:
                await ctx.reply(file=File(f, 'koala.png'), mention_author=True)

    # i have a feeling im making this more complicated than it needs to be - FDG
    @commands.command(description="Turn a provided image into an impact font meme using the syntax: toptext|bottomtext", brief="Turns an image into an impact font meme")
    async def meme(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        # Resolve command arguments and uploaded file
        file_url, meme_text = await resolve_args(ctx, args, ctx.message.attachments)
        is_gif = '.gif' in file_url or 'https://tenor.com/' in file_url

        # Download the image
        with open(f"{dannybot}\\cache\\meme_in.png", 'wb') as f:
            f.write(requests.get(file_url).content)

        png_path = f"{dannybot}\\cache\\meme_in.png"

        # Split the meme text by top and bottom and capitalize it
        if "|" in meme_text:
            meme_text_splitted = meme_text.split("|")
            top_text = meme_text_splitted[0].upper()
            bottom_text = meme_text_splitted[1].upper()
        else:
            top_text = meme_text.upper()
            bottom_text = ""

        # Create meme (gif or png)
        if is_gif:
            with open(f"{dannybot}\\cache\\gif.gif", 'wb') as f:
                f.write(requests.get(file_url).content)

            unpack_gif(f"{dannybot}\\cache\\gif.gif")
            make_meme_gif(top_text, bottom_text)
            repack_gif()
        else:
            make_meme(top_text, bottom_text, png_path)

        # Send the meme (gif or png) in response
        if is_gif:
            with open(f"{dannybot}\\cache\\ffmpeg_out.gif", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.gif'), mention_author=True)
                cleanup_ffmpeg()
        else:
            with open(f"{dannybot}\\cache\\meme_out.png", 'rb') as f:
                await ctx.reply(file=File(f, 'meme.png'), mention_author=True)

    @commands.command(aliases=['bulge'], description="Applies a bulge effect to a provided image by a specified amount. The default value is 0.5", brief="Fisheye an image by a specified amount")
    async def explode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0] if is_float(cmd_args[0]) else 0.5

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            frames = os.listdir(f'{dannybot}\\cache\\ffmpeg')

            for frame in frames:
                if '.png' in frame:
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        img.implode(amount=-float(Effect_Value))
                        img.save(filename=f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")

            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'explode.gif'), mention_author=True)
                cleanup_ffmpeg()

        else:
            with open(f'{dannybot}\\cache\\explodein.png', 'wb') as f:
                f.write(requests.get(File_Url).content)

            with magick(filename=f'{dannybot}\\cache\\explodein.png') as img:
                img.implode(amount=-float(Effect_Value))
                img.save(filename=f'{dannybot}\\cache\\exploded.png')

            with open(f'{dannybot}\\cache\\exploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'exploded.png'), mention_author=True)
                
    @commands.command(aliases=['pinch'], description="Applies a pinch effect to a provided image by a specified amount. The default value is 0.5", brief="Reverse fisheye an image by a specified amount")
    async def implode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0] if is_float(cmd_args[0]) else 0.5

        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        if '.gif' in File_Url:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            frames = os.listdir(f'{dannybot}\\cache\\ffmpeg')

            for frame in frames:
                if '.png' in frame:
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        img.implode(amount=float(Effect_Value))
                        img.save(filename=f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")

            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'implode.gif'), mention_author=True)
                cleanup_ffmpeg()

        else:
            with open(f'{dannybot}\\cache\\impin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)

            with magick(filename=f'{dannybot}\\cache\\impin.png') as img:
                img.implode(amount=float(Effect_Value))
                img.save(filename=f'{dannybot}\\cache\\imploded.png')

            with open(f'{dannybot}\\cache\\imploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'imploded.png'), mention_author=True)
    
    @commands.command(description="Command to caption memes in the same way websites like ifunny do, where it puts a white box at the top of the image with black caption text.", brief="White box; black text caption an image")
    async def caption(self, ctx, *args):
        # Resolve command arguments and uploaded file
        image_url, meme_text = await resolve_args(ctx, args, ctx.message.attachments)
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        image_content = response.content
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)

        with open(f'{dannybot}/cache/memein.png', 'wb') as f:
            f.write(image_content)

        if '.gif' in image_url:
            with open(f'{dannybot}/cache/gif.gif', 'wb') as f:
                f.write(image_content)
            unpack_gif(f'{dannybot}/cache/gif.gif')

            for frame in os.listdir(f'{dannybot}/cache/ffmpeg'):
                if '.png' in frame:
                    os.system(f'python -m dankcli "{dannybot}/cache/ffmpeg/{frame}" "{meme_text}" --filename "{dannybot}/cache/ffmpeg/output/{frame.replace(".png", "")}')

            repack_gif()

            with open(f'{dannybot}/cache/ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.gif'), mention_author=True)
                cleanup_ffmpeg()  # delete the temporary files made from the unpacking and repacking of gifs
                f.close()
        else:
            os.system(f'python -m dankcli "{dannybot}/cache/memein.png" "{meme_text}" --filename "{dannybot}/cache/memeout"')
            with open(f'{dannybot}/cache/memeout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.png'), mention_author=True)
                f.close()

    @commands.command(description="Applies a set amount of radial blur to a provided image.", brief="Applies radial blur to an image")
    async def radial(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]

        if '.gif' in Link_To_File:  # animated
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(Link_To_File).content)

            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            frames = os.listdir(f'{dannybot}\\cache\\ffmpeg')

            for frame in frames:
                if '.png' in frame:
                    with magick(filename=f'{dannybot}\\cache\\ffmpeg\\{frame}') as img:
                        img.rotational_blur(angle=6)
                        img.save(filename=f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')

            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'radial.gif'), mention_author=True)
                cleanup_ffmpeg()

        else:  # still
            with open(f'{dannybot}\\cache\\radin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)

            with magick(filename=f'{dannybot}\\cache\\radin.png') as img:
                img.rotational_blur(angle=6)
                img.save(filename=f"{dannybot}\\cache\\radial_blur.png")

            with open(f'{dannybot}\\cache\\radial_blur.png', 'rb') as f:
                await ctx.reply(file=File(f, 'radial_blur.png'), mention_author=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(image(bot))
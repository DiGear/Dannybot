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
            
    @commands.command(aliases=['distort', 'magic'], description="Applies a liquid rescale effect to the provided image.", brief="Recreation of NotSoBots 'magik' command")
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
                    imagebounds(f"{dannybot}\\cache\\ffmpeg\\{frame}")
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

    @commands.command(aliases=['bulge'], description="Applies a bulge effect to a provided image by a specified amount. The default value is 0.5", brief="Fisheye an image by a specified amount")
    async def explode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'{dannybot}\\cache\\expin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        try:
                            img.implode(amount=-float(Effect_Value))
                        except:
                            img.implode(amount=-float(0.5))  # default value
                        img.save(filename=f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'explode.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:  # still
            with magick(filename=f'{dannybot}\\cache\\expin.png') as img:
                try:
                    img.implode(amount=-float(Effect_Value))
                except:
                    img.implode(amount=-float(0.5))  # default value

                img.save(filename=f'{dannybot}\\cache\\exploded.png')
            with open(f'{dannybot}\\cache\\exploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'exploded.png'), mention_author=True)
                f.close
                
    @commands.command(aliases=['pinch'], description="Applies a pinch effect to a provided image by a specified amount. The default value is 0.5", brief="Reverse fisheye an image by a specified amount")
    async def implode(self, ctx, *args):
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        File_Url = cmd_info[0]
        cmd_args = cmd_info[1].split(' ')
        Effect_Value = cmd_args[0]
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        if '.gif' in File_Url:  # animated
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close
        else:  # still
            with open(f'{dannybot}\\cache\\impin.png', 'wb') as f:
                f.write(requests.get(File_Url).content)
                f.close

        if '.gif' in File_Url:  # animated
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    with magick(filename=f"{dannybot}\\cache\\ffmpeg\\{frame}") as img:
                        try:
                            img.implode(amount=float(Effect_Value))
                        except:
                            img.implode(amount=float(0.5))  # default value
                        img.save(filename=f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            repack_gif()

            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'implode.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:  # still
            with magick(filename=f'{dannybot}\\cache\\impin.png') as img:
                try:
                    img.implode(amount=-float(Effect_Value))
                except:
                    img.implode(amount=-float(0.5))  # default value

                img.save(filename=f'{dannybot}\\cache\\imploded.png')
            with open(f'{dannybot}\\cache\\imploded.png', 'rb') as f:
                await ctx.reply(file=File(f, 'imploded.png'), mention_author=True)
                f.close
                
    @commands.command(description="Command to caption memes in the same way websites like ifunny do, where it puts a white box at the top of the image with black caption text.", brief="White box; black text caption an image")
    async def caption(self, ctx, context, *, meme_text: typing.Optional[str] = "ValueError"):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        with open(f'{dannybot}\\cache\memein.png', 'wb') as f:
            try:  # this assume the image was linked to, and attempts to download the file via the link
                f.write(requests.get(context).content)
                f.close
            except:  # if false
                if ctx.message.attachments:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = ctx.message.attachments[0].url
                    f.write(requests.get(context).content)
                    f.close
                else:
                    print(meme_text)  # displays the contents of meme_text
                    # interpret the context variable as the meme text to be used in the command instead
                    meme_text_Fallback_Value = context
                    # displays the contents of meme_text again
                    print(meme_text_Fallback_Value)
                    meme_text = context + " " + meme_text  # merge the two values
                    if ("ValueError" in meme_text):  # error handler if the meme text cant be found
                        # honesly i don't know what the fuck its doing here
                        meme_text = meme_text_Fallback_Value
                    print(meme_text)
                    context = await message_history_img_handler(ctx)
                    f.write(requests.get(context).content)
                    f.close
        if '.gif' in context:
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(context).content)
                f.close
            # convert the gif for frames for processing
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    os.system(f'python -m dankcli "{dannybot}\\cache\\ffmpeg\\{frame}" "{meme_text}" --filename "{dannybot}\\cache\\ffmpeg\\output\\{str(frame).replace(".png", "")}')
            repack_gif()
            # prepare the file for sending
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.gif'), mention_author=True)
                cleanup_ffmpeg()  # delete the temporary files made from the unpacking and repacking of gifs
                f.close
        else:
            os.system(f'python -m dankcli "{dannybot}\\cache\\memein.png" "{meme_text}" --filename "{dannybot}\\cache\\memeout"')
            # prepare the file for sending
            with open(f'{dannybot}\\cache\memeout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'caption.png'), mention_author=True)
                f.close
                
    @commands.command(description="Applies a set amount of radial blur to a provided image.", brief="Applies radial blur to an image")
    async def radial(self, ctx, *args):
        await ctx.send("Processing. Please wait... This can take a while for GIF files.", delete_after=5)
        cmd_info = await resolve_args(ctx, args, ctx.message.attachments)
        Link_To_File = cmd_info[0]
        if '.gif' in Link_To_File:  # animated
            with open(f'{dannybot}\\cache\\gif.gif', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
        else:  # still
            with open(f'{dannybot}\\cache\\radin.png', 'wb') as f:
                f.write(requests.get(Link_To_File).content)
                f.close
        if '.gif' in Link_To_File:  # animated
            unpack_gif(f'{dannybot}\\cache\\gif.gif')
            for frame in os.listdir(f'{dannybot}\\cache\\ffmpeg'):
                if '.png' in frame:
                    with magick(filename=f'{dannybot}\\cache\\ffmpeg\\{frame}') as img:
                        img.rotational_blur(angle=6)
                        img.save(filename=f'{dannybot}\\cache\\ffmpeg\\output\\{frame}')
            repack_gif()
            with open(f'{dannybot}\\cache\\ffmpeg_out.gif', 'rb') as f:
                await ctx.reply(file=File(f, 'radial.gif'), mention_author=True)
                cleanup_ffmpeg()
                f.close
        else:  # still
            with magick(filename=f'{dannybot}\\cache\\radin.png') as img:
                img.rotational_blur(angle=6)
                img.save(filename=f"{dannybot}\\cache\\radout.png")
            with open(f'{dannybot}\\cache\\radout.png', 'rb') as f:
                await ctx.reply(file=File(f, 'radial_blur.png'), mention_author=True)
                f.close

async def setup(bot: commands.Bot):
    await bot.add_cog(image(bot))
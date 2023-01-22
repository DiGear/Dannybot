# primary function of the meme command
# take an image and put centered and outlined impact font text with a black outline over the top and bottom of the image
def make_meme(Top_Text, Bottom_Text, path):
    img = PIL.Image.open(path)

    # make sure the image is within the configured lower and upper caps
    # lower cap
    if img.size[0] < MemeWidth_LowerCap:
        ratio = (MemeWidth_LowerCap/float(img.size[0]))
        new_height = int((float(img.size[1])*float(ratio)))
        img = img.resize((MemeWidth_LowerCap, new_height), Image.Resampling.LANCZOS)
        img.save(path) # save image with new size
        img = PIL.Image.open(path) # reopen the image

    # upper cap
    if img.size[0] > MemeWidth_UpperCap:
        ratio = (MemeWidth_UpperCap/float(img.size[0]))
        new_height = int((float(img.size[1])*float(ratio)))
        img = img.resize((MemeWidth_UpperCap, new_height), Image.Resampling.LANCZOS)
        img.save(path) # save image with new size
        img = PIL.Image.open(path) # reopen the image
        
    # scale and position the text
    fontSize = int(img.size[0])
    font = ImageFont.truetype(f"{dannybot}\\assets\\impactjpn.otf", fontSize)
    topTextSize = font.getsize(Top_Text)
    bottomTextSize = font.getsize(Bottom_Text)
    while topTextSize[0] > img.size[0]-20 or bottomTextSize[0] > img.size[0]-20:
        fontSize = fontSize - 1
        topTextSize = font.getsize(Top_Text)
        bottomTextSize = font.getsize(Bottom_Text)
        break
    if fontSize  <= 0:
        fontSize = 1
    topTextPositionX = (img.size[0]/2) - (topTextSize[0]/2)
    topTextPosition = (topTextPositionX, 0)
    bottomTextPositionX = (img.size[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = img.size[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY - 10)

    # FIXED THE FUCKING STROKE SIZE - FDG
    # idk why i never bothered to calculate stroke size like this
    # it divides the size of both top and bottom text by 75 and uses that as the stroke size
    # also we make sure the stroke size is AT LEAST 1
    top_outline = int((topTextSize[0]//75))
    bottom_outline = int((bottomTextSize[0]//75))
    if top_outline <= 0:
        top_outline = 1
    if bottom_outline <= 0:
        bottom_outline = 1

    # draw the text
    draw = ImageDraw.Draw(img)
    draw.text(topTextPosition, Top_Text, (255, 255, 255), font=font,
              stroke_width=top_outline, stroke_fill=(0, 0, 0))
    draw.text(bottomTextPosition, Bottom_Text, (255, 255, 255),
              font=font, stroke_width=bottom_outline, stroke_fill=(0, 0, 0))

    # save the resulting image
    img.save(f"{dannybot}\\cache\\meme_out.png")
    return

# gif version
def make_meme_gif(Top_Text, Bottom_Text):

    # iterate through every frame in the ffmpeg folder and edit them
    for frame in os.listdir(f"{dannybot}\\cache\\ffmpeg\\"):
        if '.png' in frame:

            # open image in PIL
            img = PIL.Image.open(f"{dannybot}\\cache\\ffmpeg\\{frame}")
            path = f"{dannybot}\\cache\\ffmpeg\\{frame}"

            # make sure the image is within the configured lower and upper caps
            # lower cap
            if img.size[0] < MemeWidth_LowerCap:
                ratio = (MemeWidth_LowerCap/float(img.size[0]))
                new_height = int((float(img.size[1])*float(ratio)))
                img = img.resize((MemeWidth_LowerCap, new_height), Image.Resampling.LANCZOS)
                img.save(path) # save image with new size
                img = PIL.Image.open(path) # reopen the image

            # upper cap
            if img.size[0] > MemeWidth_UpperCap:
                ratio = (MemeWidth_UpperCap/float(img.size[0]))
                new_height = int((float(img.size[1])*float(ratio)))
                img = img.resize((MemeWidth_UpperCap, new_height), Image.Resampling.LANCZOS)
                img.save(path) # save image with new size
                img = PIL.Image.open(path) # reopen the image
            
            # fixed font size calc
            # proportionally scales the font to the size of the image, and make sure it doesn't equal 0
            imageSize = img.size
            fontSize = int(imageSize[1]/5)
            if fontSize  <= 0:
                fontSize = 1

            font = ImageFont.truetype(
                f"{dannybot}\\assets\\impactjpn.otf", fontSize)

            # scale and position the text
            topTextSize = font.getsize(Top_Text)
            bottomTextSize = font.getsize(Bottom_Text)
            topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
            topTextPosition = (topTextPositionX, 0)
            bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
            bottomTextPositionY = imageSize[1] - bottomTextSize[1]
            bottomTextPosition = (bottomTextPositionX, bottomTextPositionY - 10)

            # FIX THE FUCKING STROKE SIZE - FDG
            # idk why i never bothered to calculate stroke size like this
            # it divides the size of both top and bottom text by 75 and uses that as the stroke size
            # also we make sure the stroke size is AT LEAST 1
            top_outline = int((topTextSize[0]//75))
            bottom_outline = int((bottomTextSize[0]//75))
            if top_outline <= 0:
                top_outline = 1
            if bottom_outline <= 0:
                bottom_outline = 1

            # draw the text
            draw = ImageDraw.Draw(img)
            draw.text(topTextPosition, Top_Text, (255, 255, 255), font=font,
                    stroke_width=top_outline, stroke_fill=(0, 0, 0))
            draw.text(bottomTextPosition, Bottom_Text, (255, 255, 255),
                    font=font, stroke_width=bottom_outline, stroke_fill=(0, 0, 0))

            # save the resulting image
            img.save(f"{dannybot}\\cache\\ffmpeg\\output\\{frame}")
            print("frame " + frame + " processed")
    repack_gif()
    return
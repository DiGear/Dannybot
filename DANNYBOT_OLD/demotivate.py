from PIL import Image, ImageDraw, ImageFont
from sys import argv


def demotivator(image: str, toptext: str, bottomtext: str = ""):
    topfnt = ImageFont.truetype(font="./assets/font.ttf", size=80)
    btmfnt = ImageFont.truetype(font="./assets/font.ttf", size=50)
    demotivator = PIL.Image.open("./assets/template.png")
    pastein = PIL.Image.open(image)
    pastein = pastein.resize((1056, 564))
    W, H = demotivator.size
    demotivator.paste(pastein, (118, 79))
    draw = ImageDraw.Draw(demotivator)
    if len(toptext) >= 19:
        topfnt = ImageFont.truetype(font="./assets/font.ttf", size=65)
    elif len(toptext) >= 28:
        topfnt = ImageFont.truetype(font="./assets/font.ttf", size=50)
    T1w, T1h = draw.textsize(toptext, topfnt)
    txt1 = draw.text((int((W - T1w) / 2), 700), toptext, font=topfnt)
    T2w, T2h = draw.textsize(bottomtext, btmfnt)
    txt1 = draw.text((int((W - T2w) / 2), 850), bottomtext, font=btmfnt)
    demotivator.save("./demotivate.png")


if len(argv) >= 4:
    demotivator(argv[1], argv[2], bottomtext=argv[3])
else:
    demotivator(argv[1], argv[2])
from config import *

logger = logging.getLogger(__name__)

# make sure we have a profiles directory
PROFILE_DIR = f"{dannybot}\\profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

# gets or creates a user profile from json
def get_user_profile(member: discord.Member):
        profile_path = os.path.join(PROFILE_DIR, f"{member.id}.json")

        if not os.path.exists(profile_path):
            # set up default profile values for new users
            default_profile = {
                "level": 1,
                "experience_current": 0,
                "experience_total": 10 
            }
            with open(profile_path, "w") as f:
                json.dump(default_profile, f, indent=4)
    
        with open(profile_path, "r") as f:
            return json.load(f)

# saves the profile data back to json
def save_user_profile(member: discord.Member, profile_data):
        profile_path = os.path.join(PROFILE_DIR, f"{member.id}.json")
        with open(profile_path, "w") as f:
            json.dump(profile_data, f, indent=4)

# handles xp gain and level ups
def add_experience(member: discord.Member, xp: int):
        profile = get_user_profile(member)
        profile["experience_current"] += xp
        leveled_up = False

        # check if we need to level up
        while profile["experience_current"] >= profile["experience_total"]:
            profile["experience_current"] -= profile["experience_total"]
            profile["level"] += 1
            profile["experience_total"] = int(profile["experience_total"] * 1.25)
            leveled_up = True

        save_user_profile(member, profile)
        return leveled_up

# numbers
def abbreviate_xp(xp):
    if xp >= 1e300: # not quite the limit of 10^308, but close enough and i dont want it to be too close to the limit idk why i just dont want it to
        return "inf"
    elif xp >= 1e13:
        return f"{xp:.2e}" # too big
    elif xp >= 1e12:
        return f"{xp / 1e12:.2f}T"   # trillion
    elif xp >= 1e9:
        return f"{xp / 1e9:.2f}B"    # billion
    elif xp >= 1e6:
        return f"{xp / 1e6:.2f}M"    # million
    elif xp >= 1e3:
        return f"{xp / 1e3:.2f}K"    # thousand
    else:
        return str(xp)

class Stats(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot
            # load fonts for the profile card
            font_path = os.path.join(dannybot, "assets", "futura.ttf")
            self.font_large = ImageFont.truetype(font_path, 32)
            self.font_small = ImageFont.truetype(font_path, 20)

        @commands.hybrid_command(name="profile")
        async def profile(self, ctx, member: discord.Member = None):
            # use author if no member specified
            if member is None:
                member = ctx.author

            # get all the user data we need
            user_data = get_user_profile(member)
            nickname = member.display_name
            level = user_data.get("level", 1)
            xp_current = user_data.get("experience_current", 0)
            xp_total = user_data.get("experience_total", 100)

            # abbreviate the XP values
            xp_current_abbr = abbreviate_xp(xp_current)
            xp_total_abbr = abbreviate_xp(xp_total)

            # get avatar and banner urls
            avatar_url = member.guild_avatar.url if member.guild_avatar else member.display_avatar.url
            fallback_banner_url = "https://t3.ftcdn.net/jpg/01/71/05/82/360_F_171058201_KFR9cLbr3VKoQIFtGFY7t9PvfmdXjv5t.jpg"
            user = await ctx.bot.fetch_user(member.id)
            banner_url = user.banner.url if user.banner else fallback_banner_url

            # download and process banner image
            response_banner = requests.get(banner_url)
            banner_img = Image.open(BytesIO(response_banner.content)).convert("RGBA")

            # download and process avatar image
            response_avatar = requests.get(avatar_url)
            avatar_img = Image.open(BytesIO(response_avatar.content)).convert("RGBA")

            # make the avatar circular
            avatar_size = (128, 128)
            avatar_img = avatar_img.resize(avatar_size, Image.LANCZOS)
            mask = Image.new("L", avatar_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)
            avatar_img = ImageOps.fit(avatar_img, mask.size, centering=(0.5, 0.5))
            avatar_img.putalpha(mask)

            # create the base card
            card_width = 600
            card_height = 250
            card = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 0))

            # paste banner as full background
            banner_resized = banner_img.resize((card_width, card_height), Image.LANCZOS)
            card.paste(banner_resized, (0, 0))

            # overlay white on the bottom half
            draw = ImageDraw.Draw(card)
            draw.rectangle([0, card_height // 2-8, card_width, card_height], fill="white")

            # create black outline for avatar
            outline_size = 136
            outline = Image.new("RGBA", (outline_size, outline_size), (0, 0, 0, 0))
            draw_outline = ImageDraw.Draw(outline)
            draw_outline.ellipse((0, 0, outline_size, outline_size), fill="black")

            # paste outline first
            avatar_x = 30
            avatar_y = 30
            card.paste(outline, (avatar_x - 4, avatar_y - 4), outline)

            # paste avatar on top
            card.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

            # function to draw text with an outline
            def draw_text_with_outline(draw, position, text, font, text_color="white", outline_color="black", outline_thickness=2):
                x, y = position

                # draw outline (8 directions)
                for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness), (0, outline_thickness),
                               (-outline_thickness, -outline_thickness), (-outline_thickness, outline_thickness),
                               (outline_thickness, -outline_thickness), (outline_thickness, outline_thickness)]:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

                # draw main text
                draw.text((x, y), text, font=font, fill=text_color)

            # draw nickname with outline
            text_x = avatar_x + 140
            text_y = avatar_y + 10
            draw_text_with_outline(draw, (text_x, text_y), nickname, self.font_large)

            # draw level and xp
            text_y += 40
            level_text = f"Level {level} | {xp_current_abbr}/{xp_total_abbr} DP"
            draw_text_with_outline(draw, (text_x, text_y), level_text, self.font_small)

            # draw xp progress bar
            bar_width = 300
            bar_height = 20
            bar_x = text_x
            bar_y = text_y + 40
            draw.rectangle([bar_x-4, bar_y-4, bar_x+4 + bar_width, bar_y+4 + bar_height], outline=(0, 0, 0), width=4)
            xp_ratio = xp_current / xp_total if xp_total != 0 else 0
            fill_width = int(bar_width * xp_ratio)
            fill_color = (66, 135, 245)
            draw.rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], fill=fill_color)

            # save and send the image
            with BytesIO() as image_binary:
                card.save(image_binary, "PNG")
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename="profile.png"))
    
        @commands.is_owner()
        @commands.command(name="addxp", hidden=True)
        async def addxp(self, ctx, xp: int, member: discord.Member = None):
            member = member or ctx.author
            # check for valid xp amount
            if xp <= 0 or xp > 1e301: # higher than the abbreviated max int so it can reach inf
                await ctx.send("xp gain error")
                return

            # add xp and check for level up
            leveled_up = add_experience(member, xp)
            if leveled_up:
                user_data = get_user_profile(member)
                level = user_data.get("level", 1)
                await ctx.send(f"you fucking moron idiot you just leveled up to level {level} **(d.profile)**")
                return

async def setup(bot: commands.Bot):
        await bot.add_cog(Stats(bot))

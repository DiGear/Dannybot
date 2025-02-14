# profiles testing
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
                "experience_total": 100 
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

class Profiles(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot
            # load fonts for the profile card
            font_path = os.path.join(dannybot, "assets", "futura.ttf")
            self.font_large = ImageFont.truetype(font_path, 32)
            self.font_small = ImageFont.truetype(font_path, 20)

        @commands.command(name="profile")
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

            # add banner to card
            banner_resized = banner_img.resize((card_width, card_height), Image.LANCZOS)
            card.paste(banner_resized, (0, 0))

            # add avatar to card
            avatar_x = 30
            avatar_y = 30
            card.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

            # add text elements
            draw = ImageDraw.Draw(card)
            text_x = avatar_x + 140
            text_y = avatar_y + 10
            draw.text((text_x, text_y), nickname, font=self.font_large, fill="white")
            text_y += 40
            level_text = f"Level {level} | {xp_current}/{xp_total} XP"
            draw.text((text_x, text_y), level_text, font=self.font_small, fill="white")

            # draw xp progress bar
            bar_width = 300
            bar_height = 20
            bar_x = text_x
            bar_y = text_y + 40
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline=(255, 255, 255), width=2)
            xp_ratio = xp_current / xp_total if xp_total != 0 else 0
            fill_width = int(bar_width * xp_ratio)
            fill_color = (66, 135, 245)
            draw.rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], fill=fill_color)

            # save and send the image
            with BytesIO() as image_binary:
                card.save(image_binary, "PNG")
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename="profile.png"))

        @commands.command(name="addxp")
        async def addxp(self, ctx, xp: int):
            # check for valid xp amount
            if xp <= 0:
                await ctx.send("xp gain error")
                return

            # add xp and check for level up
            leveled_up = add_experience(ctx.author, xp)
            if leveled_up:
                await ctx.send("level up")
                return

async def setup(bot: commands.Bot):
        await bot.add_cog(Profiles(bot))

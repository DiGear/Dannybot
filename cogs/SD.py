# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)

# Load the JSON
with open(f"{dannybot}\\assets\\stable_diffusion_config.json") as f:
    SD_Config = json.load(f)

# Load JSON params
lora = SD_Config["lora"]
nsfw_lora = SD_Config["nsfw_lora"]

# checkpoint translator keys
checkpoints = {
    "3D Animation": "3D.safetensors",
    "AOM3": "abyssorangemix3AOM3_aom3a1b.safetensors",
    "AnimUWU Ultimate": "animuwultimate145.safetensors",
    "Anything v3": "anythingV3_fp16.ckpt",
    "Anything v5": "AnythingV5Ink_v5PrtRE.safetensors",
    "AnyLoRA": "anyloraCheckpoint_bakedvaeBlessedFp16.safetensors",
    "CafeMix MIA": "madeinabyssCafemix_v10.safetensors",
    "Exquisite Details": "exquisiteDetails_art.safetensors",
    "Made In Abyss": "MIA 704 120rp 1e-6.ckpt",
    "Realistic (SD 1.5 Base)": "SD_1.5_Base.safetensors",
    "RichyRichMix": "richyrichmix_V2Fp16.safetensors",
    "Sayori (Nekopara) Artstyle": "SayoriDiffusion.ckpt",
    "Sonic-Diffusion": "sonicdiffusion_v3Beta4.safetensors",
}

# VAE translator keys
vaes = {
    "Automatic": "nothingvae.safetensors",
    "vaeFtMse840000": "vaeFtMse840000.safetensors",
    "Danny VAE": "VAE.vae.pt",
}

class sd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="sd",
        description="Create AI generated images via Stable-Diffusion.",
        brief="Create AI generated images with Dannybot.",
    )
    async def stablediffusion(
        self,
        ctx: commands.Context,
        *,
        positive_prompt: str,
        negative_prompt: str = "lowres, bad anatomy, bad hands, text, missing fingers, extra digit, fewer digits",
        steps: int = 12,
        sampler: Literal[
        "DDIM",
        "DDPM",
        "DDPM Karras",
        "DPM adaptive",
        "DPM fast",
        "DPM++ 2M",
        "DPM++ 2M Karras",
        "DPM++ 2M SDE",
        "DPM++ 2M SDE Turbo",
        "DPM++ 3M SDE",
        "DPM++ 3M SDE Karras",
        "DPM++ SDE",
        "DPM++ SDE Karras",
        "Euler",
        "Euler A Turbo",
        "Euler a",
        "Heun",
        "LCM",
        "LCM Karras",
        "LMS",
        "LMS Karras",
        "PLMS",
        "Restart",
        "UniPC"
    ] = "Euler A Turbo",
        cfg: float = 7.0,
        seed: int = -1,
        grid_size: int = 1,
        width: int = 1,
        height: int = 1,
        checkpoint: Literal[
            "3D Animation",
            "AOM3",
            "AnimUWU Ultimate",
            "Anything v3",
            "Anything v5",
            "AnyLoRA",
            "CafeMix MIA",
            "Exquisite Details",
            "Made In Abyss",
            "Realistic (SD 1.5 Base)",
            "RichyRichMix",
            "Sayori (Nekopara) Artstyle",
            "Sonic-Diffusion",
        ] = "Anything v5",
        vae: Literal[
            "Automatic",
            "None",
            "vaeFtMse840000",
            "Danny VAE",
        ] = "None",
        clip_skip: int = 2, 
        #bool: bool = True
    ):
        await ctx.defer()
            
        if seed == -1:
            seed = random.randint(0,999999999)
        
        """
        anti [REDACTED] measures
        """

        # defining size defaults
        if height == 1:
            height == 512
            
        if width == 1:
            width == 512
        
        cfg = round(cfg, 1)
        cfg = min(max(cfg, 0.5), 30.0)
        
        grid_size = min(max(grid_size, 1), 4)
        #denoise = min(max(denoise, 0.001), 1.000)
        
        steps = max(1, min(steps, 150))
        
        height = min(max(height, 64), 1024)
        width = min(max(width, 64), 1024)

        """
        end anti [REDACTED] measures
        """
        
        #--------------
        # LORA shit
        #--------------
        positive_prompt2 = positive_prompt
        activeloras = []
        lora_weight = []

        try:
            isNSFWChannel = isinstance(ctx.channel, discord.DMChannel) or ctx.channel.nsfw
        except:
            isNSFWChannel = False

        loraconcat = loraconcatnsfw if isNSFWChannel else loraconcatsfw
        
        lora_tags = {}
        found_loras_string = ""
        used_loras = []

        for lora_tuple in loraconcat:
            lora_name = lora_tuple[0]
            pattern = r'\b' + re.escape(lora_name) + r'\b'
            if re.search(pattern, positive_prompt2, re.IGNORECASE):
                name, strength = lora_tuple[1], lora_tuple[2]
                lora_tag = f"<lora:{name}:{strength}> {lora_name}"
                positive_prompt2 = re.sub(pattern, lora_tag, positive_prompt2, flags=re.IGNORECASE)
                used_loras.append((lora_name.capitalize(), strength))

        output_prompt = positive_prompt2
        found_loras_string = ", ".join([f"{lora[0]} ({lora[1]})" for lora in used_loras])
        #--------------
        # End LORA Shit
        #--------------
        
        # getting the checkpoint value from the dictionary
        checkpoint_alias = checkpoint
        if checkpoint_alias in checkpoints:
            checkpoint_alias = checkpoints[checkpoint_alias]

        # getting the VAE value from the dictionary
        vae_alias = vae
        if vae_alias in vaes:
            vae_alias = vaes[vae_alias]
     
        #defining stuff for the command
        sd_url = "http://127.0.0.1:7860"
        
        payload = {
        "prompt": output_prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "sampler_name": sampler,
         "batch_size": grid_size,
        "cfg_scale": cfg,
        "seed": seed,
        "width": width,
        "height": height,
        #this is for me :)
        "save_images": True
        }
        
        #these are specific overrides
        override_settings = {
        "sd_model_checkpoint": checkpoint_alias,
        "sd_vae": vae_alias,
        "CLIP_stop_at_last_layers": clip_skip
        }

        #apply the overrides
        payload["override_settings"] = override_settings
        print(payload)
        
        # actually generate the image
        response = requests.post(url=f'{sd_url}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        
        #we use this as an ID of sorts
        iteration_seed = str(uuid.uuid4())
        image_path = f"{dannybot}\\cache\\SD_OUT\\{ctx.author.name}-sd-{iteration_seed}.png"
        image.save(image_path)
        
        # Prepare the generated image for embed
        embed = discord.Embed(title="img2img", color=0x80FFFF)
        embed.set_image(url=f"attachment://{ctx.author.name}-sd-{iteration_seed}.png")
        embed.set_footer(text=f"UUID: {iteration_seed}")
        embed.set_author(
            name=ctx.author.name, icon_url=ctx.author.avatar.url
        )
        
        if found_loras_string == "":
            found_loras_string = "None"

        # setting up the embed fields
        embed_fields = [
            ("User Positive Prompt", f"{positive_prompt[: 1024 - 3]}", False),
            ("SD Internal Positive Prompt", f"{output_prompt[: 1024 - 3]}", False),
            ("Negative Prompt", f"{negative_prompt[: 1024 - 3]}", False),
            ("Checkpoint Model", checkpoint, False),
            ("VAE Model", vae, False),
            ("Triggered LORAs", f"{found_loras_string[: 1024 - 3]}", False),
            ("CFG Scale", cfg, True),
            ("Resolution",f"{width}x{height}",True,),
            ("Clip Skip",str(clip_skip),True,),
            ("Sampler",f"{sampler}",True,),
            ("Sampling Steps", steps, True),
            ("Seed", seed, True),
            ("Grid Size", grid_size, True),
            #("Denoise", denoise, True),
        ]

        # looping over the embed fields and adding them one by one to the embed object
        for name, value, inline in embed_fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Send embed and file together
        with open(image_path, "rb") as image_file:
            image_data = discord.File(image_file, filename=f"{ctx.author.name}-sd-{iteration_seed}.png")
            await ctx.reply(embed=embed, file=image_data)
       
    @commands.hybrid_command(
        name="loras",
        description="View the list of LORAs supported by Dannybots stable-diffusion command.",
        brief="Show LORA list",
    )
    async def loralist(self, ctx: commands.Context):
        await ctx.defer()

        def process_lora_list(main_list):
            return ", ".join(str(key[0]) for key in sorted(main_list, key=lambda x: x[0]))

        lora_list = lora
        loraXL_list = loraXL

        is_nsfw = isinstance(ctx.channel, discord.TextChannel) and ctx.channel.nsfw

        if is_nsfw:
            lora_list += nsfw_lora

        lora_output = process_lora_list(lora_list)

        await ctx.send(f"SD 1.X:\n{lora_output}")

    @commands.hybrid_command(
        name="checkpoints",
        description="View the list of Checkpoints supported by Dannybots stable-diffusion command.",
        brief="Show Checkpoint list",
    )
    async def checkpoints(self, ctx: commands.Context):
        await ctx.defer()
        keys_sorted = sorted(checkpoints.keys())
        keys_string = ", ".join(keys_sorted)
        await ctx.send(str(keys_string))

async def setup(bot: commands.Bot):
    await bot.add_cog(sd(bot))

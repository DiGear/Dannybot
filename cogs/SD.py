# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)

# Load the JSON
with open(f"{dannybot}\\assets\\stable_diffusion_config.json") as f:
    SD_Config = json.load(f)

# Load JSON params
lora = SD_Config["lora"]
nsfw_lora = SD_Config["nsfw_lora"]
loraXL = SD_Config["loraXL"]
nsfw_loraXL = SD_Config["nsfw_loraXL"]

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
    # XL SHIT
    "Crystal Clear XL": "crystalClearXL_ccxl.safetensors",
    "Hassaku XL": "hassakuXLSfwNsfw_alphaV05.safetensors",
    "Kohaku XL": "kohakuXL_nyan.safetensors",
    "Nekoray XL": "nekorayxl_v06W3.safetensors",
    "Realistic (SDXL Base)": "sd_xl_base_1.0_0.9vae.safetensors",
}

# VAE translator keys
vaes = {
    "From Model": "nothingvae.safetensors",
    "vaeFtMse840000": "vaeFtMse840000.safetensors",
    "Danny VAE": "VAE.vae.pt",
}


class sd(commands.Cog):
    DefaultLora = SD_Config["default_lora"]
    SD_Queue = []
    # the address of the server to connect to
    server_address = "127.0.0.1:8188"

    # UUID to use when hooking up to the server
    client_id = str(uuid.uuid4())

    def __init__(self, bot: commands.Bot):
        try:
            self.bot = bot
            self.ws = websocket.WebSocket()
            self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
            self.SD_Task_Loop.start()
        except:
            print("Could not connect to the stable-diffusion-webui-forge instance.")
            pass
        
    @commands.hybrid_command(
        name="loras",
        description="View the list of LORAs supported by Dannybots stable-diffusion command.",
        brief="Show LORA list",
    )
    async def loralist(self, ctx: commands.Context):
        await ctx.defer()

        def process_lora_list(main_list):
            return ", ".join(
                str(key[0]) for key in sorted(main_list, key=lambda x: x[0])
            )

        is_nsfw = (
            False if isinstance(ctx.channel, discord.DMChannel) else ctx.channel.nsfw
        )

        if is_nsfw:
            lora_output = process_lora_list(lora + nsfw_lora)
            loraXL_output = process_lora_list(loraXL + nsfw_loraXL)
        else:
            lora_output = process_lora_list(lora)
            loraXL_output = process_lora_list(loraXL)

        await ctx.send(f"SD 1.X:\n{lora_output}\n\nSDXL:\n{loraXL_output}")

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

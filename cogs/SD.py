# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class sd(commands.Cog):
    server_address = "127.0.0.1:8188"
    client_id = str(uuid.uuid4())

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

    @commands.hybrid_command(
        name="sd",
        aliases=["grok", "diffuse", "stablediffusion"],
        description="Create AI generated images via Stable-Diffusion.",
        brief="Create AI generated images with Dannybot.",
    )
    async def stablediffusion(
        self,
        ctx: commands.Context,
        *,
        cfg: float = 7.000,
        denoise: float = 1.000,
        width: int = 512,
        height: int = 512,
        checkpoint: Literal[
            "Default", "Anything", "Sayori (Nekopara) Artstyle", "Sonic Artstyle"
        ] = "Anything",
        positive_prompt: str,
        negative_prompt: str = "lowres, bad anatomy, bad hands, text, missing fingers, extra digit, fewer digits",
        sampler: Literal[
            "euler",
            "euler_ancestral",
            "heun",
            "dpm_2",
            "dpm_2_ancestral",
            "Ims",
            "dpm_fast",
            "dpm_adaptive",
            "dpmpp_2s_ancestral",
            "dpmpp_sde",
            "dpmpp_sde_gpu",
            "dpmpp_2m",
            "dpmpp_2m_sde",
            "dpmpp_2m_sde_gpu",
            "ddim",
            "uni_pc",
            "uni_pc_bh2",
        ] = "uni_pc",
        scheduler: Literal[
            "normal", "karras", "exponential", "simple", "ddim_uniform"
        ] = "normal",
        seed: int = 11223344556677889900112233,  # idk how else to do this
        steps: int = 15,
    ):
        await ctx.defer()
        seed = (
            random.randint(0, 999999999) if seed == 11223344556677889900112233 else seed
        )
        steps = max(1, min(steps, 50))
        height = min(max(height, 64), 1024)
        width = min(max(width, 64), 1024)
        denoise = min(max(denoise, 0.001), 1.000)
        checkpoints = {
            "Anything": "anythingV3_fp16.ckpt",
            "Sayori (Nekopara) Artstyle": "SayoriDiffusion.ckpt",
            "Default": "SD_1.5_Base.safetensors",
            "Sonic Artstyle": "sonicdiffusion_v3Beta4.safetensors",
        }
        checkpoint_alias = checkpoint
        if checkpoint_alias in checkpoints:
            checkpoint_alias = checkpoints[checkpoint_alias]
        generator_values = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": denoise,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": sampler,
                    "scheduler": scheduler,
                    "seed": seed,
                    "steps": steps,
                },
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": checkpoint_alias},
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {"batch_size": 1, "height": height, "width": width},
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": positive_prompt},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": negative_prompt},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]},
            },
        }

        prompt = generator_values.copy()
        images = self.get_images(self.ws, prompt)
        latent_image = (prompt["5"]["inputs"]["width"], prompt["5"]["inputs"]["height"])
        negative = prompt["7"]["inputs"]["text"]
        positive = prompt["6"]["inputs"]["text"]
        inputs_values = prompt["3"]["inputs"]
        cfg, denoise, sampler_name, scheduler, seed, steps = [
            inputs_values[key]
            for key in ["cfg", "denoise", "sampler_name", "scheduler", "seed", "steps"]
        ]
        embed_fields = [
            ("Positive Prompt", positive, False),
            ("Negative Prompt", negative, False),
            ("CFG Scale", cfg, True),
            ("Denoise", denoise, True),
            ("Resolution", f"{latent_image[0]}x{latent_image[1]}", True),
            ("Checkpoint", checkpoint, True),
            ("Sampler", sampler_name, True),
            ("Scheduler", scheduler, True),
            ("Seed", seed, True),
            ("Steps", steps, True),
        ]
        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data))
                with io.BytesIO() as out:
                    image.save(out, format="png")
                    out.seek(0)
                    file = discord.File(fp=out, filename="image.png")
                    embed = discord.Embed()
                    for name, value, inline in embed_fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    embed.set_image(url="attachment://image.png")
                    await ctx.send(embed=embed, file=file)

    def queue_prompt(self, prompt):
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt",
            data=ujson.dumps({"prompt": prompt, "client_id": self.client_id}).encode(
                "utf-8"
            ),
        )
        return ujson.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        with urllib.request.urlopen(
            f"http://{self.server_address}/view?{urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': folder_type})}"
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            f"http://{self.server_address}/history/{prompt_id}"
        ) as response:
            return ujson.loads(response.read())

    def get_images(self, ws, prompt):
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = ujson.loads(out)
                if message.get("type") == "executing":
                    data = message.get("data")
                    if data.get("node") is None and data.get("prompt_id") == prompt_id:
                        break
        history = self.get_history(prompt_id)[prompt_id]
        outputs = history.get("outputs", {})
        for node_id, node_output in outputs.items():
            if "images" in node_output:
                images_output = [
                    self.get_image(image["filename"], image["subfolder"], image["type"])
                    for image in node_output["images"]
                ]
                output_images[node_id] = images_output
        return output_images


async def setup(bot: commands.Bot):
    await bot.add_cog(sd(bot))

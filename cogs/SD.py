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
        aliases=["grok", "diffuse"],
        description="Create AI generated images via Stable-Diffusion.",
        brief="Create AI generated images with Dannybot.",
    )
    async def sd(
        self,
        ctx: commands.Context,
        *,
        cfg: float = 7.0,
        denoise: float = 1.0,
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
        ] = "euler_ancestral",
        scheduler: Literal[
            "normal", "karras", "exponential", "simple", "ddim_uniform"
        ] = "ddim_uniform",
        seed: int = None,
        steps: int = 20,
    ):
        await ctx.defer()
        seed = random.randint(0, 999999999) if seed is None else seed
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
                    "cfg": 7,
                    "denoise": 1,
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
        prompt["6"]["inputs"]["text"] = f"{positive_prompt}"
        prompt["3"]["inputs"]["seed"] = random.randint(0, 9999999999)
        images = self.get_images(self.ws, prompt)
        cfg = prompt["3"]["inputs"]["cfg"]
        denoise = prompt["3"]["inputs"]["denoise"]
        latent_image = (prompt["5"]["inputs"]["width"], prompt["5"]["inputs"]["height"])
        model = prompt["4"]["inputs"]["ckpt_name"]
        negative = prompt["7"]["inputs"]["text"]
        positive = prompt["6"]["inputs"]["text"]
        sampler_name = prompt["3"]["inputs"]["sampler_name"]
        scheduler = prompt["3"]["inputs"]["scheduler"]
        seed = prompt["3"]["inputs"]["seed"]
        steps = prompt["3"]["inputs"]["steps"]

        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data))
                out = io.BytesIO()
                image.save(out, format="png")
                out.seek(0)
                file = discord.File(out, "image.png")
                embed = discord.Embed(title="Stable Diffusion Output")
                embed.set_image(url="attachment://image.png")
                embed.add_field(name="Positive Prompt", value=positive, inline=False)
                embed.add_field(name="Negative Prompt", value=negative, inline=False)
                embed.add_field(name="CFG Scale", value=cfg, inline=True)
                embed.add_field(name="Denoise", value=denoise, inline=True)
                embed.add_field(
                    name="Resolution",
                    value=f"{latent_image[0]}x{latent_image[1]}",
                    inline=True,
                )
                embed.add_field(name="Checkpoint", value=model, inline=True)
                embed.add_field(name="Sampler", value=sampler_name, inline=True)
                embed.add_field(name="Scheduler", value=scheduler, inline=True)
                embed.add_field(name="Seed", value=seed, inline=True)
                embed.add_field(name="Steps", value=steps, inline=True)

                await ctx.send(embed=embed, file=file)

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode("utf-8")
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(
            f"http://{self.server_address}/view?{url_values}"
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            f"http://{self.server_address}/history/{prompt_id}"
        ) as response:
            return json.loads(response.read())

    def get_images(self, ws, prompt):
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message["type"] == "executing":
                    data = message["data"]
                    if data["node"] is None and data["prompt_id"] == prompt_id:
                        break
            else:
                continue

        history = self.get_history(prompt_id)[prompt_id]
        for o in history["outputs"]:
            for node_id in history["outputs"]:
                node_output = history["outputs"][node_id]
                if "images" in node_output:
                    images_output = []
                    for image in node_output["images"]:
                        image_data = self.get_image(
                            image["filename"], image["subfolder"], image["type"]
                        )
                        images_output.append(image_data)
                output_images[node_id] = images_output
        return output_images


async def setup(bot: commands.Bot):
    await bot.add_cog(sd(bot))

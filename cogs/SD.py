# LORA-test

# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)


class sd(commands.Cog):
    # the address of the server to connect to
    server_address = "127.0.0.1:8188"
    # UUID to use when hooking up to the server
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
        seed: int = 11223344556677889900112233,  # fuck
        steps: int = 15,
    ):
        await ctx.defer()
        # if the seed is that bullshit default value, it will generate a random seed
        seed = (
            random.randint(0, 999999999) if seed == 11223344556677889900112233 else seed
        )
        # trimming CFG value in range of 0.001 to 1.000
        cfg = min(max(cfg, 0.001), 100.000)
        # trimming steps value in range of 1 to 50
        steps = max(1, min(steps, 50))
        # trimming width and height value in range of 64 to 1024
        height = min(max(height, 64), 1024)
        width = min(max(width, 64), 1024)
        # trimming denoise value in range of 0.001 to 1.000
        denoise = min(max(denoise, 0.001), 1.000)
        # translator for simplified checkpoint names to the actual filenames
        checkpoints = {
            "Anything": "anythingV3_fp16.ckpt",
            "Sayori (Nekopara) Artstyle": "SayoriDiffusion.ckpt",
            "Default": "SD_1.5_Base.safetensors",
            "Sonic Artstyle": "sonicdiffusion_v3Beta4.safetensors",
        }
        # getting the checkpoint value from the above dictionary
        checkpoint_alias = checkpoint
        if checkpoint_alias in checkpoints:
            checkpoint_alias = checkpoints[checkpoint_alias]
        # LORA translator (part of LORA-test branch)
        lora = {
            "senko": "Senko-San.safetensors",
            "astolfo": "Astolfo.safetensors",
            "kiryu": "Kiryu Kazuma.safetensors",
            "megumin": "megumin.safetensors",
            "izuna": "izuna.safetensors",
            "fumo": "Fumo.pt",
            "shitty": "jaggy_lines_noise_taged-000012.safetensors",
            "the cat": "Karyl.safetensors",
            "karyl": "Karyl.safetensors",
            "remilia": "Remilia Scarlet.safetensors",
            "sans": "Sans.safetensors",
            "slime": "slimegirls.safetensors",
            "sylph": "Sylph.safetensors",
            "yuno": "Yuno Gasai.safetensors",
            "touhou": "Zun Style.safetensors",
            "neptunia": "TSNeptunia-000045.safetensors",
            "neptune": "Neptune.safetensors",
            "kanade": "Kanade Tachibana.safetensors",
            "tenshi": "Kanade Tachibana.safetensors",
            "hu tao": "hu tao.safetensors",
            "hand": "GoodHands-beta2.safetensors",
        }
        # lora matching logic
        activeloras = []
        for key in lora.keys():
            if key in positive_prompt.lower():
                activeloras.append(lora[key])
        if not activeloras:
            activeloras = ["GoodHands-beta2.safetensors"]
        # a dictionary which acts as the configuration for the image generation
        generator_values = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": denoise,
                    "latent_image": ["5", 0],
                    "model": ["10", 0],
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
                "inputs": {"clip": ["10", 1], "text": positive_prompt},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["10", 1], "text": negative_prompt},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]},
            },
            "10": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": activeloras[-1],
                    "strength_model": 0.75,
                    "strength_clip": 1,
                    "model": ["4", 0],
                    "clip": ["4", 1],
                },
            },
        }

        # extracts values from the dict and assigns them to variables so we can use them in the embed
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
        # setting up the embed fields
        embed_fields = [
            ("Positive Prompt", positive, False),
            ("Negative Prompt", negative, False),
            ("Checkpoint", checkpoint, False),
            ("Active LORA(s)", activeloras[-1].split(".")[0], False),
            ("CFG Scale", cfg, True),
            ("Denoise", denoise, True),
            ("Resolution", f"{latent_image[0]}x{latent_image[1]}", True),
            ("Sampler", sampler_name, True),
            ("Scheduler", scheduler, True),
            ("Seed", seed, True),
            ("Steps", steps, True),
        ]
        # fetch and prepare the generated image for embed
        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data))
                with io.BytesIO() as out:
                    image.save(out, format="png")
                    out.seek(0)
                    # preparing the data to be send on discord
                    file = discord.File(fp=out, filename="image.png")
                    embed = discord.Embed()
                    # looping over the embed fields and adding them one by one to the embed object
                    for name, value, inline in embed_fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    embed.set_image(url="attachment://image.png")
                    await ctx.send(embed=embed, file=file)

    def queue_prompt(self, prompt):
        # making a request to the server for a new prompt. it contains the new prompt and client id, encoded in UTF-8 (THIS IS IMPORTANT)
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt",
            data=ujson.dumps({"prompt": prompt, "client_id": self.client_id}).encode(
                "utf-8"
            ),
        )
        # send the request to the server and get the response
        return ujson.loads(urllib.request.urlopen(req).read())

    def get_filename(self, filename, subfolder, folder_type):
        # open a connection to the server with the provided parameters (filename, subfolder, type) to retrieve the requested file
        with urllib.request.urlopen(
            f"http://{self.server_address}/view?{urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': folder_type})}"
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        # open a connection to the server using the ID of the prompt to retrieve its history
        with urllib.request.urlopen(
            f"http://{self.server_address}/history/{prompt_id}"
        ) as response:
            return ujson.loads(response.read())

    def get_images(self, ws, prompt):
        # queue a new prompt for execution
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        # enter an infinite loop until we receive the target data from WebSocket.
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = ujson.loads(out)
                if message.get("type") == "executing":
                    data = message.get("data")
                    # check if the node is None and prompt_id matches with our prompt_id; if it does, break the loop.
                    if data.get("node") is None and data.get("prompt_id") == prompt_id:
                        break
        # return a dictionary holding the history of the prompt execution including outputs.
        history = self.get_history(prompt_id)[prompt_id]
        # extract the outputs from the history.
        outputs = history.get("outputs", {})
        # go through each output entry in the outputs.
        for node_id, node_output in outputs.items():
            # check if there are any images in the node_output.
            if "images" in node_output:
                # gets images from server for each image in the node_output.
                images_output = [
                    self.get_filename(
                        image["filename"], image["subfolder"], image["type"]
                    )
                    for image in node_output["images"]
                ]
                # add the received images to the output_images dictionary using node_id as the key.
                output_images[node_id] = images_output
        return output_images


async def setup(bot: commands.Bot):
    await bot.add_cog(sd(bot))

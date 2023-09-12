# if you can't find a variable used in this file its probably imported from here
from config import *

logger = logging.getLogger(__name__)

# LORA translator keys
lora = [
    ("senko", "Senko-San.safetensors", 1.0),
    ("astolfo", "Astolfo.safetensors", 1.0),
    ("kiryu", "Kiryu Kazuma.safetensors", 1.0),
    ("megumin", "megumin.safetensors", 1.0),
    ("izuna", "izuna.safetensors", 1.0),
    ("fumo", "Fumo.pt", 1.0),
    ("shitty", "jaggy_lines_noise_taged-000012.safetensors", 1.3),
    ("the cat", "Karyl.safetensors", 1.0),
    ("karyl", "Karyl.safetensors", 1.0),
    ("remilia", "Remilia Scarlet.safetensors", 1.0),
    ("sans", "Sans.safetensors", 0.85),
    ("slime", "slimegirls.safetensors", 1.0),
    ("sylph", "Sylph.safetensors", 0.9),
    ("yuno", "Yuno Gasai.safetensors", 0.9),
    ("touhou", "Zun Style.safetensors", 1.0),
    ("neptunia", "TSNeptunia-000045.safetensors", 1.0),
    ("neptune", "Neptune.safetensors", 0.85),
    ("kanade", "Kanade Tachibana.safetensors", 0.85),
    ("tenshi", "Kanade Tachibana.safetensors", 0.85),
    ("hu tao", "hu tao.safetensors", 0.85),
    ("hand", "GoodHands-beta2.safetensors", 1.0),
    ("compa", "compa_v2-000009.safetensors", 0.66),
    ("ryouna", "ryouna.pt", 0.75),
    ("leffrey", "leffrey.pt", 1.0),
    ("detailed", "add_detail.safetensors", 0.75),
    ("among us", "Among Us.safetensors", 1.0),
    ("good eyes", "beautifuleyes.safetensors", 0.85),
    ("canonome", "Camonome Style.safetensors", 1.0),
    ("chara", "Chara.safetensors", 0.8),
    ("chibi", "Chibi Style.safetensors", 0.7),
    ("danganronpa", "Danganronpa Style.safetensors", 0.75),
    ("feet", "feet 2.safetensors", 0.75),
    ("figure", "Figurine.safetensors", 1.0),
    ("anya face", "Anya Face.safetensors", 0.9),
    ("gaping", "gape.safetensors", 0.7),
    ("gigachad", "Gigachad.safetensors", 0.7),
    ("made in abyss", "Made In Abyss Style.safetensors", 0.7),
    ("mgq", "Monster Girl Quest.safetensors", 1.0),
    ("omori", "Omori.safetensors", 0.45),
    ("nanachi", "Nanachi.safetensors", 0.7),
    ("shrift", "Nekomata Style.safetensors", 1.2),
    ("papi", "Papi.safetensors", 0.85),
    ("toka", "tokacomics.safetensors", 1.0),
    ("scout", "scoutv3.safetensors", 0.7),
    ("natsuki", "Natsuki_V1.safetensors", 0.7),
    ("yuri", "YuriV1.safetensors", 0.7),
    ("monika", "MonikaV1.safetensors", 0.7),
    ("sayori", "Sayori_V1.safetensors", 0.7),
    ("teto", "kasanetetoV3-10.safetensors", 0.85),
    ("shrugging", "concept_shrugging-11.safetensors", 1.0),
    ("chungus", "bigchungus.pt", 0.5),
    ("afrobull", "afrobull-000018.safetensors", 0.7),
    ("goblin girl", "gobGirlzLora.pt", 1.3),
    ("caracal", "floppa Caracal.pt", 0.75),
    ("lucky star", "lucky_star_offset.safetensors", 0.93),
]


# checkpoint translator keys
checkpoints = {
    "3D Animation": "3D.safetensors",
    "AOM2 (NSFW)": "abyssorangemix2_Hard.safetensors",
    "AOM3": "abyssorangemix3AOM3_aom3a1b.safetensors",
    "Anything v3": "anythingV3_fp16.ckpt",
    "Anything v5": "AnythingV5Ink_v5PrtRE.safetensors",
    "AnyLoRA": "anyloraCheckpoint_bakedvaeBlessedFp16.safetensors",
    "CafeMix MIA": "madeinabyssCafemix_v10.safetensors",
    "Made In Abyss": "MIA 704 120rp 1e-6.ckpt",
    "Realistic": "SD_1.5_Base.safetensors",
    "RichyRichMix": "richyrichmix_V2Fp16.safetensors",
    "Sayori (Nekopara) Artstyle": "SayoriDiffusion.ckpt",
    "Sonic-Diffusion": "sonicdiffusion_v3Beta4.safetensors",
}

# VAE translator keys
vaes = {
    "From Model": "nothingvae.safetensors",
    "vaeFtMse840000": "vaeFtMse840000.safetensors",
    "Danny VAE": "VAE.vae.pt",
}


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
        name="loras",
        description="View the list of LORAs supported by Dannybots stable-diffusion command.",
        brief="Show LORA list",
    )
    async def loralist(self, ctx: commands.Context):
        await ctx.defer()
        keys_sorted = sorted(lora, key=lambda x: x[0])
        keys_string = ", ".join([str(key[0]) for key in keys_sorted])
        await ctx.send(keys_string)

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
        positive_prompt: str,
        negative_prompt: str = "lowres, bad anatomy, bad hands, text, missing fingers, extra digit, fewer digits",
        cfg: float = 7.000,
        denoise: float = 1.000,
        batch_size: int = 1,
        width: int = 512,
        height: int = 512,
        checkpoint: Literal[
            "3D Animation",
            "AOM2 (NSFW)",
            "AOM3",
            "Anything v3",
            "Anything v5",
            "AnyLoRA",
            "CafeMix MIA",
            "Made In Abyss",
            "Realistic",
            "RichyRichMix",
            "Sayori (Nekopara) Artstyle",
            "Sonic-Diffusion",
        ] = "Anything v5",
        vae: Literal[
            "From Model",
            "vaeFtMse840000",
            "Danny VAE",
        ] = "From Model",
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
            "dpmpp_sde_gpu",
            "dpmpp_2m",
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

        # init this
        batch_processed = 0

        """
        anti cris measures
        """

        # trimming CFG value in range of 0.001 to 100.000
        cfg = min(max(cfg, 0.001), 100.000)
        # trimming Batch Size value in range of 1 to 4
        batch_size = min(max(batch_size, 1), 4)
        # trimming Denoise value in range of 0.001 to 1.000
        denoise = min(max(denoise, 0.001), 1.000)
        # trimming steps value in range of 1 to 50
        steps = max(1, min(steps, 50))
        # trimming width and height value in range of 64 to 1024
        height = min(max(height, 64), 1024)
        width = min(max(width, 64), 1024)

        """
        end anti cris measures
        """

        # getting the checkpoint value from the dictionary
        checkpoint_alias = checkpoint
        if checkpoint_alias in checkpoints:
            checkpoint_alias = checkpoints[checkpoint_alias]

        # getting the VAE value from the dictionary
        vae_alias = vae
        if vae_alias in vaes:
            vae_alias = vaes[vae_alias]

        # lora matching logic
        activeloras = []
        lora_weight = []
        for lora_tuple in lora:
            if lora_tuple[0] in positive_prompt.lower():
                activeloras.append(lora_tuple[1])
                lora_weight.append(lora_tuple[2])
        if not activeloras:
            activeloras = ["GoodHands-beta2.safetensors"]
            lora_weight = [1]

        # a dictionary which acts as the configuration for the image generation
        generator_values = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": denoise,
                    "latent_image": ["5", 0],
                    "model": ["13", 0],
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
                "inputs": {"batch_size": batch_size, "height": height, "width": width},
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["13", 1], "text": positive_prompt},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["13", 1], "text": negative_prompt},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["0", 0],
                },
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "Dannybot_" + ctx.author.name,
                    "images": ["8", 0],
                },
            },
            "10": {
                "class_type": "VAELoader",
                "inputs": {"vae_name": vae_alias},
            },
            "11": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": activeloras[0],
                    "strength_model": lora_weight[0],
                    "strength_clip": 1,
                    "model": ["4", 0],
                    "clip": ["4", 1],
                },
            },
            "12": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": "GoodHands-beta2.safetensors"
                    if len(activeloras) < 2
                    else activeloras[1],
                    "strength_model": lora_weight[1] if len(lora_weight) >= 2 else 0,
                    "strength_clip": 0 if len(activeloras) < 2 else 1,
                    "model": ["11", 0],
                    "clip": ["11", 1],
                },
            },
            "13": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": "GoodHands-beta2.safetensors"
                    if len(activeloras) < 3
                    else activeloras[2],
                    "strength_model": lora_weight[2] if len(lora_weight) >= 3 else 0,
                    "strength_clip": 0 if len(activeloras) < 3 else 1,
                    "model": ["12", 0],
                    "clip": ["12", 1],
                },
            },
        }

        # vae shit
        if vae == "From Model":
            generator_values["8"]["inputs"]["vae"] = ["4", 2]
        else:
            generator_values["8"]["inputs"]["vae"] = ["10", 0]

        # extracts values from the dict and assigns them to variables so we can use them in the embed
        prompt = generator_values.copy()
        images = self.get_images(self.ws, prompt)
        latent_image = (prompt["5"]["inputs"]["width"], prompt["5"]["inputs"]["height"])
        batch_size = prompt["5"]["inputs"]["batch_size"]
        negative = prompt["7"]["inputs"]["text"]
        positive = prompt["6"]["inputs"]["text"]
        inputs_values = prompt["3"]["inputs"]
        lora_list_for_embed = ""
        for i in range(len(activeloras)):
            lora_list_for_embed += (
                str(activeloras[i]).replace(".safetensors", "").replace(".pt", "")
            )
            lora_list_for_embed += " (" + str(float(lora_weight[i])) + "), "
        cfg, denoise, sampler_name, scheduler, seed, steps = [
            inputs_values[key]
            for key in ["cfg", "denoise", "sampler_name", "scheduler", "seed", "steps"]
        ]

        sampler_name = sampler_name.replace("_", " ")

        # fetch and prepare the generated image for embed
        for node_id in images:
            for image_data in images[node_id]:
                batch_processed += 1
                image = Image.open(io.BytesIO(image_data))
                with io.BytesIO() as out:
                    image.save(out, format="png")
                    out.seek(0)

                    # preparing the data to be send on discord
                    file = discord.File(fp=out, filename="image.png")
                    embed = discord.Embed(title="txt2img", color=0x80FFFF)
                    embed.set_image(url="attachment://image.png")
                    embed.set_footer(text=f"Seed: {seed}")
                    embed.set_author(
                        name=ctx.author.name, icon_url=ctx.author.avatar.url
                    )

                    # setting up the embed fields
                    embed_fields = [
                        ("Positive Prompt", positive[: 1024 - 3], False),
                        ("Negative Prompt", negative[: 1024 - 3], False),
                        ("Checkpoint Model", checkpoint, False),
                        ("VAE Model", vae, False),
                        (
                            "Additional Networks (lora, loha, lokr, locon)",
                            lora_list_for_embed,
                            False,
                        ),
                        ("CFG Scale", cfg, True),
                        (
                            "Resolution",
                            f"{latent_image[0]}x{latent_image[1]}",
                            True,
                        ),
                        ("Batch Count", f"{batch_processed} of {batch_size}", True),
                        ("Sampling method", f"{sampler_name} {scheduler}", True),
                        ("Sampling Steps", steps, True),
                        ("Denoise", denoise, True),
                    ]

                    # debugging stuff
                    print(activeloras)
                    print(lora_weight)
                    print(vae)
                    print(vae_alias)
                    print(embed_fields)

                    # looping over the embed fields and adding them one by one to the embed object
                    for name, value, inline in embed_fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await ctx.reply(embed=embed, file=file)

    # making a request to the server for a new prompt. it contains the new prompt and client id, encoded in UTF-8 (THIS IS IMPORTANT)
    def queue_prompt(self, prompt):
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt",
            data=ujson.dumps({"prompt": prompt, "client_id": self.client_id}).encode(
                "utf-8"
            ),
        )

        # send the request to the server and get the response
        return ujson.loads(urllib.request.urlopen(req).read())

    # open a connection to the server with the provided parameters (filename, subfolder, type) to retrieve the requested file
    def get_filename(self, filename, subfolder, folder_type):
        with urllib.request.urlopen(
            f"http://{self.server_address}/view?{urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': folder_type})}"
        ) as response:
            return response.read()

    # open a connection to the server using the ID of the prompt to retrieve its history
    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            f"http://{self.server_address}/history/{prompt_id}"
        ) as response:
            return ujson.loads(response.read())

    # queue a new prompt for execution
    def get_images(self, ws, prompt):
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

        # gets images from server for each image in the node_output.
        for node_id, node_output in outputs.items():
            if "images" in node_output:
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

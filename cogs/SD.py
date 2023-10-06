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
    "Anything v3": "anythingV3_fp16.ckpt",
    "Anything v5": "AnythingV5Ink_v5PrtRE.safetensors",
    "AnyLoRA": "anyloraCheckpoint_bakedvaeBlessedFp16.safetensors",
    "CafeMix MIA": "madeinabyssCafemix_v10.safetensors",
    "Made In Abyss": "MIA 704 120rp 1e-6.ckpt",
    "Realistic (SD 1.5 Base)": "SD_1.5_Base.safetensors",
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
    DefaultLora = SD_Config["default_lora"]
    SD_Queue = []
    # the address of the server to connect to
    server_address = "127.0.0.1:8188"

    # UUID to use when hooking up to the server
    client_id = str(uuid.uuid4())

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
        self.SD_Task_Loop.start()

    # make sure we stop the task loop before reloading the cog
    def cog_unload(self):
        self.SD_Task_Loop.cancel()

    # task loops and executes items in the SD queue without overlap, interrupting when the cog is reloaded.
    @tasks.loop(seconds=1.0)
    async def SD_Task_Loop(self):
        # Check if there is even anything in the queue first before trying to do anything.
        if len(self.SD_Queue) > 0:
            # Look at the queue and get the first one in line
            current_prompt = self.SD_Queue[0]
            # Remove the item from the queue so it doesnt do the same task endlessly
            self.SD_Queue.pop(0)

            # Each element in SD_Queue contains all necessary information (prompt, activeloras, lora_weight, cfg, denoise, scheduler, seed, steps, message_id, author_id, batch_processed) to pass onto the task loop.

            # Retrieve the variables from the queue. I could probably do this better
            prompt = current_prompt["prompt"]
            activeloras = current_prompt["activeloras"]
            lora_weight = current_prompt["lora_weight"]
            cfg = current_prompt["cfg"]
            denoise = current_prompt["denoise"]
            scheduler = current_prompt["scheduler"]
            seed = current_prompt["seed"]
            steps = current_prompt["steps"]
            ctx = current_prompt["ctx"]
            author_id = current_prompt["author_id"]
            batch_processed = current_prompt["batch_processed"]
            checkpoint = current_prompt["checkpoint"]
            vae = current_prompt["vae"]
            vae_alias = current_prompt["vae_alias"]
            batch_size = current_prompt["batch_size"]

            author = self.bot.get_user(author_id)

            # This code runs the "get_images" function in the executor, allowing it to wait for completion in this task without blocking the slash command.
            images = await self.bot.loop.run_in_executor(
                None, self.get_images, self.ws, prompt
            )

            if current_prompt["type"] == "txt2img":
                # images = self.get_images(self.ws, prompt)
                latent_image = (
                    prompt["5"]["inputs"]["width"],
                    prompt["5"]["inputs"]["height"],
                )
                batch_size = prompt["5"]["inputs"]["batch_size"]
                negative = prompt["7"]["inputs"]["text"]
                positive = prompt["6"]["inputs"]["text"]
                inputs_values = prompt["3"]["inputs"]
                lora_list_for_embed = ""
                for i in range(min(5, len(activeloras))):
                    lora_list_for_embed += (
                        str(activeloras[i])
                        .replace(".safetensors", "")
                        .replace(".pt", "")
                    )
                    lora_list_for_embed += " (" + str(float(lora_weight[i])) + "), "
                    if lora_list_for_embed.startswith("GoodHands-beta2 (0.0),"):
                        lora_list_for_embed = "none"
                cfg, denoise, sampler_name, scheduler, seed, steps = [
                    inputs_values[key]
                    for key in [
                        "cfg",
                        "denoise",
                        "sampler_name",
                        "scheduler",
                        "seed",
                        "steps",
                    ]
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
                                name=author.name, icon_url=author.avatar.url
                            )

                            # setting up the embed fields
                            embed_fields = [
                                ("Positive Prompt", positive[: 1024 - 3], False),
                                ("Negative Prompt", negative[: 1024 - 3], False),
                                ("Checkpoint Model", checkpoint, False),
                                ("VAE Model", vae, False),
                                (
                                    "Additional Networks",
                                    lora_list_for_embed,
                                    False,
                                ),
                                ("CFG Scale", cfg, True),
                                (
                                    "Resolution",
                                    f"{latent_image[0]}x{latent_image[1]}",
                                    True,
                                ),
                                (
                                    "Batch Count",
                                    f"{batch_processed} of {batch_size}",
                                    True,
                                ),
                                (
                                    "Sampling method",
                                    f"{sampler_name} {scheduler}",
                                    True,
                                ),
                                ("Sampling Steps", steps, True),
                                ("Denoise", denoise, True),
                            ]

                            # looping over the embed fields and adding them one by one to the embed object
                            for name, value, inline in embed_fields:
                                embed.add_field(name=name, value=value, inline=inline)
                            await ctx.reply(embed=embed, file=file)
            else:
                negative = prompt["7"]["inputs"]["text"]
                positive = prompt["6"]["inputs"]["text"]
                inputs_values = prompt["4"]["inputs"]
                lora_list_for_embed = ""
                for i in range(min(5, len(activeloras))):
                    lora_list_for_embed += (
                        str(activeloras[i])
                        .replace(".safetensors", "")
                        .replace(".pt", "")
                    )
                    lora_list_for_embed += " (" + str(float(lora_weight[i])) + "), "
                    if lora_list_for_embed.startswith("GoodHands-beta2 (0.0),"):
                        lora_list_for_embed = "none"
                cfg, denoise, sampler_name, scheduler, seed, steps = [
                    inputs_values[key]
                    for key in [
                        "cfg",
                        "denoise",
                        "sampler_name",
                        "scheduler",
                        "seed",
                        "steps",
                    ]
                ]

                sampler_name = sampler_name.replace("_", " ")

                # fetch and prepare the generated image for embed
                for node_id in images:
                    for image_data in images[node_id]:
                        image = Image.open(io.BytesIO(image_data))
                        with io.BytesIO() as out:
                            image.save(out, format="png")
                            out.seek(0)

                            # preparing the data to be send on discord
                            file = discord.File(fp=out, filename="image.png")
                            embed = discord.Embed(title="img2img", color=0x80FFFF)
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
                                    "Additional Networks",
                                    lora_list_for_embed,
                                    False,
                                ),
                                ("CFG Scale", cfg, True),
                                (
                                    "Sampling method",
                                    f"{sampler_name} {scheduler}",
                                    True,
                                ),
                                ("Sampling Steps", steps, True),
                                ("Denoise", denoise, True),
                            ]

                            # looping over the embed fields and adding them one by one to the embed object
                            for name, value, inline in embed_fields:
                                embed.add_field(name=name, value=value, inline=inline)
                            await ctx.reply(embed=embed, file=file)

    @commands.hybrid_command(
        name="loras",
        description="View the list of LORAs supported by Dannybots stable-diffusion command.",
        brief="Show LORA list",
    )
    async def loralist(self, ctx: commands.Context):
        await ctx.defer()
        try:
            if isinstance(ctx.channel, discord.DMChannel) or not ctx.channel.nsfw:
                blahstodo = lora
            else:
                blahstodo = lora + nsfw_lora
        except:
            blahstodo = lora
        keys_sorted = sorted(blahstodo, key=lambda x: x[0])
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
            "AOM3",
            "Anything v3",
            "Anything v5",
            "AnyLoRA",
            "CafeMix MIA",
            "Made In Abyss",
            "Realistic (SD 1.5 Base)",
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
        steps: int = 24,
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
        loraconcat = lora + nsfw_lora
        try:
            if isinstance(ctx.channel, discord.DMChannel) or not ctx.channel.nsfw:
                for lora_tuple in lora:
                    if lora_tuple[0] in positive_prompt.lower():
                        activeloras.append(lora_tuple[1])
                        lora_weight.append(lora_tuple[2])
            else:
                for lora_tuple in loraconcat:
                    if lora_tuple[0] in positive_prompt.lower():
                        activeloras.append(lora_tuple[1])
                        lora_weight.append(lora_tuple[2])
        except:
            for lora_tuple in lora:
                if lora_tuple[0] in positive_prompt.lower():
                    activeloras.append(lora_tuple[1])
                    lora_weight.append(lora_tuple[2])

        if not activeloras:
            activeloras = [self.DefaultLora]
            lora_weight = [0]

        # a dictionary which acts as the configuration for the image generation
        generator_values = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": denoise,
                    "latent_image": ["5", 0],
                    "model": ["15", 0],
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
                "inputs": {"clip": ["15", 1], "text": positive_prompt},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["15", 1], "text": negative_prompt},
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
                    "filename_prefix": "Dannybot_txt2img_" + ctx.author.name,
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
                    "lora_name": self.DefaultLora
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
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 3
                    else activeloras[2],
                    "strength_model": lora_weight[2] if len(lora_weight) >= 3 else 0,
                    "strength_clip": 0 if len(activeloras) < 3 else 1,
                    "model": ["12", 0],
                    "clip": ["12", 1],
                },
            },
            "14": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 4
                    else activeloras[3],
                    "strength_model": lora_weight[3] if len(lora_weight) >= 4 else 0,
                    "strength_clip": 0 if len(activeloras) < 4 else 1,
                    "model": ["13", 0],
                    "clip": ["13", 1],
                },
            },
            "15": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 5
                    else activeloras[4],
                    "strength_model": lora_weight[4] if len(lora_weight) >= 5 else 0,
                    "strength_clip": 0 if len(activeloras) < 5 else 1,
                    "model": ["14", 0],
                    "clip": ["14", 1],
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

        prompt_ToQueue = {
            "prompt": prompt,
            "activeloras": activeloras,
            "lora_weight": lora_weight,
            "cfg": cfg,
            "denoise": denoise,
            "scheduler": scheduler,
            "seed": seed,
            "steps": steps,
            "ctx": ctx,
            "author_id": ctx.author.id,
            "batch_processed": batch_processed,
            "vae": vae,
            "checkpoint": checkpoint,
            "batch_size": batch_size,
            "vae_alias": vae_alias,
            "type": "txt2img",
        }

        self.SD_Queue.append(prompt_ToQueue)

    @commands.hybrid_command(
        name="img2img",
        description="Create AI generated images via Stable-Diffusion img2img.",
        brief="Create AI generated images with Dannybot using img2img.",
    )
    async def stablediffusionimg2img(
        self,
        ctx: commands.Context,
        *,
        positive_prompt: str,
        image: discord.Attachment,
        negative_prompt: str = "lowres, bad anatomy, bad hands, text, missing fingers, extra digit, fewer digits",
        cfg: float = 7.000,
        denoise: float = 0.670,
        checkpoint: Literal[
            "3D Animation",
            "AOM3",
            "Anything v3",
            "Anything v5",
            "AnyLoRA",
            "CafeMix MIA",
            "Made In Abyss",
            "Realistic (SD 1.5 Base)",
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
        steps: int = 24,
    ):
        await ctx.defer()
        # if the seed is that bullshit default value, it will generate a random seed
        seed = (
            random.randint(0, 999999999) if seed == 11223344556677889900112233 else seed
        )

        path = f"{dannybot}\\cache\\img2img.png"
        response = requests.get(image.url)
        with open(path, "wb") as file:
            file.write(response.content)
        image = PIL.Image.open(path)
        w, h = image.size
        nw, nh = (768, int(h * 768 / w)) if w > h else (int(w * 768 / h), 768)
        scaled_image = image.resize((max(min(nw, w), 1), max(min(nh, h), 1)))
        scaled_image.save(path)

        """
        anti cris measures
        """

        # trimming CFG value in range of 0.001 to 100.000
        cfg = min(max(cfg, 0.001), 100.000)
        # trimming Denoise value in range of 0.001 to 1.000
        denoise = min(max(denoise, 0.001), 1.000)
        # trimming steps value in range of 1 to 50
        steps = max(1, min(steps, 50))

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
        loraconcat = lora + nsfw_lora
        if isinstance(ctx.channel, discord.DMChannel) or not ctx.channel.nsfw:
            for lora_tuple in lora:
                if lora_tuple[0] in positive_prompt.lower():
                    activeloras.append(lora_tuple[1])
                    lora_weight.append(lora_tuple[2])
        else:
            for lora_tuple in loraconcat:
                if lora_tuple[0] in positive_prompt.lower():
                    activeloras.append(lora_tuple[1])
                    lora_weight.append(lora_tuple[2])

        if not activeloras:
            activeloras = [self.DefaultLora]
            lora_weight = [0]

        # a dictionary which acts as the configuration for the image generation
        generator_values = {
            "2": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": f"{dannybot}\\cache\\img2img.png",
                    "choose file to upload": "image",
                },
            },
            "3": {
                "class_type": "VAEEncode",
                "inputs": {"pixels": ["2", 0], "vae": ["0", 0]},
            },
            "4": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": cfg,
                    "denoise": denoise,
                    "latent_image": ["3", 0],
                    "model": ["15", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": sampler,
                    "scheduler": scheduler,
                    "seed": seed,
                    "steps": steps,
                },
            },
            "5": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": checkpoint_alias},
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["15", 1], "text": positive_prompt},
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["15", 1], "text": negative_prompt},
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["4", 0],
                    "vae": ["0", 0],
                },
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "Dannybot_img2img_" + ctx.author.name,
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
                    "model": ["5", 0],
                    "clip": ["5", 1],
                },
            },
            "12": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": self.DefaultLora
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
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 3
                    else activeloras[2],
                    "strength_model": lora_weight[2] if len(lora_weight) >= 3 else 0,
                    "strength_clip": 0 if len(activeloras) < 3 else 1,
                    "model": ["12", 0],
                    "clip": ["12", 1],
                },
            },
            "14": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 4
                    else activeloras[3],
                    "strength_model": lora_weight[3] if len(lora_weight) >= 4 else 0,
                    "strength_clip": 0 if len(activeloras) < 4 else 1,
                    "model": ["13", 0],
                    "clip": ["13", 1],
                },
            },
            "15": {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": self.DefaultLora
                    if len(activeloras) < 5
                    else activeloras[4],
                    "strength_model": lora_weight[4] if len(lora_weight) >= 5 else 0,
                    "strength_clip": 0 if len(activeloras) < 5 else 1,
                    "model": ["14", 0],
                    "clip": ["14", 1],
                },
            },
        }

        # vae shit
        if vae == "From Model":
            generator_values["8"]["inputs"]["vae"] = ["5", 2]
            generator_values["3"]["inputs"]["vae"] = ["5", 2]
        else:
            generator_values["8"]["inputs"]["vae"] = ["10", 0]
            generator_values["3"]["inputs"]["vae"] = ["10", 0]

        # extracts values from the dict and assigns them to variables so we can use them in the embed
        prompt = generator_values.copy()

        prompt_ToQueue = {
            "prompt": prompt,
            "activeloras": activeloras,
            "lora_weight": lora_weight,
            "cfg": cfg,
            "denoise": denoise,
            "scheduler": scheduler,
            "seed": seed,
            "steps": steps,
            "ctx": ctx,
            "author_id": ctx.author.id,
            "batch_processed": 0,
            "vae": vae,
            "checkpoint": checkpoint,
            "batch_size": 1,
            "vae_alias": vae_alias,
            "type": "img2img",
        }

        self.SD_Queue.append(prompt_ToQueue)

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
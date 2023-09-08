# if you can't find a variable used in this file its probably imported from here
from config import *
logger = logging.getLogger(__name__)

class sd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command(name="sd", aliases=["grok", "diffuse"], description="Create AI generated images via Stable-Diffusion.", brief="Create AI generated images with Dannybot.")
    async def sd(self, ctx, *, positive_prompt:str):       
        prompt_text = """
        {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 8,
                    "denoise": 1,
                    "latent_image": [
                        "5",
                        0
                    ],
                    "model": [
                        "4",
                        0
                    ],
                    "negative": [
                        "7",
                        0
                    ],
                    "positive": [
                        "6",
                        0
                    ],
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "seed": 8566257,
                    "steps": 20
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "anythingV3_fp16.ckpt"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": 512,
                    "width": 512
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "masterpiece best quality girl"
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "bad hands"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": [
                        "3",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                }
            }
        }
        """

        def queue_prompt(prompt):
            p = {"prompt": prompt}
            data = json.dumps(p).encode('utf-8')
            req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
            request.urlopen(req)

        prompt = json.loads(prompt_text)
        seed = random.randint(0, 9999999999)
        
        #set the text prompt for our positive CLIPTextEncode
        prompt["6"]["inputs"]["text"] = f"{positive_prompt}"

        #set the seed for our KSampler node
        prompt["3"]["inputs"]["seed"] = int(seed)

        queue_prompt(prompt)

        # Wait until comfyui finished generating idk how else to do this rn
        time.sleep(5)

        list_of_files = glob.glob('I:\\ComfyUI\\ComfyUI\\output/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        
        await ctx.send(f"Generated image for prompt: '{positive_prompt}' using seed: {seed} and model: {prompt['4']['inputs']['ckpt_name']}", file=discord.File(latest_file))

async def setup(bot: commands.Bot):
    await bot.add_cog(sd(bot))
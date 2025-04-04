import os
import asyncio
import logging
import discord
from discord.ext import commands
import gradio as gr
from config import *

# global variables to share state with the gradio panel
log_list = []  # stores log messages
last_command = ""  # stores the last processed command


# custom logging handler to capture terminal output in log_list
class ListHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_list.append(log_entry)
        # limit log list size
        if len(log_list) > 1000:
            log_list.pop(0)


# set up root logging i dont fucking use this btw
logger = logging.getLogger()
logger.setLevel(logging.INFO)
list_handler = ListHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
list_handler.setFormatter(formatter)
logger.addHandler(list_handler)

# also print logs to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# create a discord bot instance
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
intents = discord.Intents.all()
bot = commands.AutoShardedBot(
    command_prefix=dannybot_prefixes,
    status=discord.Status.online,
    intents=intents,
    case_insensitive=True,
)


# function to automatically load all cogs from the "cogs" folder
async def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"loaded cog: {filename}")
            except Exception as e:
                logging.error(f"failed to load cog {filename}: {e}")


# bot is ready
@bot.event
async def on_ready():
    print("---------------------------------------------------------------------")
    if clean_pooter_onLaunch:
        print(
            Fore.LIGHTMAGENTA_EX
            + "Cleaning up pooter folder... This may clog up the terminal if there are a lot of files..."
            + Fore.RESET
        )
        print("---------------------------------------------------------------------")
        clean_pooter()
        print("---------------------------------------------------------------------")
    if cache_clear_onLaunch:
        print(
            Fore.LIGHTMAGENTA_EX
            + "Clearing cache from the previous session..."
            + Fore.RESET
        )
        print("---------------------------------------------------------------------")
        clear_cache()
        print("---------------------------------------------------------------------")
    await load_all_cogs()
    print("---------------------------------------------------------------------")
    command_sync = await bot.tree.sync()
    print(Fore.BLUE + f"Synced {len(command_sync)} slashes" + Fore.RESET)
    print("---------------------------------------------------------------------")
    print(
        Fore.GREEN
        + f"{bot.user} successfully booted on discord.py version {discord.__version__} with {bot.shard_count} shards"
        + Fore.RESET
    )
    print("---------------------------------------------------------------------")


# process messages and update the last command variable
@bot.event
async def on_message(message):
    global last_command
    if message.author == bot.user:
        return
    if any(message.content.startswith(prefix) for prefix in dannybot_prefixes):
        last_command = message.content
        os.chdir(dannybot)  # brought back from the old bot.py fle
        if random.randint(0, dannybot_denialRatio) == dannybot_denialRatio:
            await message.channel.send(
                random.choice(dannybot_denialResponses), reference=message
            )
        else:
            await bot.process_commands(message)


# ping command
@bot.hybrid_command(
    name="ping",
    description="Calculate bot latency and send the results.",
    brief="Sends the current bot latency",
)
async def ping(ctx: commands.Context):
    start_time = time.monotonic()
    message = await ctx.send("Round-trip Latency: NANms | API Latency: NANms")
    end_time = time.monotonic()
    ping_time = round((end_time - start_time) * 1000)
    await message.edit(
        content=f"Round-trip Latency: {ping_time}ms | API Latency: {round(bot.latency * 1000)}ms"
    )


@bot.hybrid_command(
    name="say", description="DEV COMMAND | No description given", hidden=True
)
async def say(ctx: commands.Context, *, text):
    if ctx.author.id not in dannybot_team_ids:
        await ctx.reply("This command is restricted.", ephemeral=True, delete_after=3)
    else:
        await ctx.reply("say command issued.", ephemeral=True, delete_after=1)
        await ctx.channel.send(text)
        try:
            await ctx.message.delete()  # this only works for text-based messages
        except Exception:
            return


# ------------------------
# discord bot functions
# ------------------------
def update_status(status_choice, activity_name, activity_type):
    status_mapping = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.do_not_disturb,
        "invisible": discord.Status.invisible,
    }
    activity_mapping = {
        "playing": discord.ActivityType.playing,
        "streaming": discord.ActivityType.streaming,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
        "competing": discord.ActivityType.competing,
    }
    selected_status = status_mapping.get(status_choice, discord.Status.online)
    selected_activity_type = activity_mapping.get(
        activity_type, discord.ActivityType.playing
    )

    async def change_presence():
        await bot.change_presence(
            status=selected_status,
            activity=discord.Activity(type=selected_activity_type, name=activity_name),
        )
        logging.info(
            f"changed status to {status_choice} with activity {activity_type}: {activity_name}"
        )

    asyncio.run_coroutine_threadsafe(change_presence(), bot.loop)
    return f"status updated to {status_choice} with activity {activity_type}: {activity_name}"


def reload_all_cogs():
    async def quick_restart():
        for ext in list(bot.extensions.keys()):
            try:
                await bot.reload_extension(ext)
                logging.info(f"reloaded cog: {ext}")
            except Exception as e:
                logging.error(f"failed to reload cog {ext}: {e}")
        await bot.tree.sync()

    asyncio.run_coroutine_threadsafe(quick_restart(), bot.loop)
    return "success"


def get_loaded_cogs():
    return list(bot.extensions.keys())


def load_cog(cog_name):
    async def load():
        try:
            await bot.load_extension(f"cogs.{cog_name}")
            logging.info(f"loaded cog: {cog_name}")
            await bot.tree.sync()
        except Exception as e:
            logging.error(f"failed to load cog {cog_name}: {e}")

    asyncio.run_coroutine_threadsafe(load(), bot.loop)
    return f"load command issued for cog: {cog_name}"


def unload_cog(cog_name):
    async def unload():
        try:
            await bot.unload_extension(f"cogs.{cog_name}")
            logging.info(f"unloaded cog: {cog_name}")
        except Exception as e:
            logging.error(f"failed to unload cog {cog_name}: {e}")

    asyncio.run_coroutine_threadsafe(unload(), bot.loop)
    return f"unload command issued for cog: {cog_name}"


def reload_cog(cog_name):
    async def reload_ext():
        try:
            await bot.reload_extension(f"cogs.{cog_name}")
            logging.info(f"reloaded cog: {cog_name}")
        except Exception as e:
            logging.error(f"failed to reload cog {cog_name}: {e}")

    asyncio.run_coroutine_threadsafe(reload_ext(), bot.loop)
    return f"reload command issued for cog: {cog_name}"


def get_log():
    return "\n".join(log_list[-100:])


def get_last_command():
    return last_command

directory_paths = {
    "Pooter Files": "database/Pooter",
    "Danny Files": "database/Danny",
    "Leffrey Files": "database/Leffrey",
    "Femboy Files": "database/Femboy",
    "Fanboy Files": "database/Fanboy",
    "Glass Cup Images": "database/Glasscup",
    "Plastic Cup Images": "database/Plasticcup",
    "Burger Files": "database/Burger",
    "Nekopara Files": "database/Nekopara",
    "Animal Girl Images": "database/Mimi",
}

def get_file_info(category):
    path = os.path.join('database', category)
    if not os.path.exists(path):
        return f"Category '{category}' not found."
    
    bag_path = f'bags/{category}_bag.json'
    if os.path.exists(bag_path):
        with open(bag_path, 'r') as f:
            bag_data = json.load(f)
        bag_remaining = len(bag_data.get(category, {}).get('bag', []))
        total_files = len(bag_data.get(category, {}).get('original_values', []))
    else:
        bag_remaining = total_files = 0
    
    file_count = len(os.listdir(path))
    size = sum(os.path.getsize(os.path.join(path, f)) for f in os.listdir(path)) / (1024 * 1024)
    
    return f"{file_count} files\nSize: {size:.2f} MB\n{bag_remaining}/{total_files} files remaining in bag"

def display_database():
    results = {cat: get_file_info(path.split('/')[-1].lower()) for cat, path in directory_paths.items()}
    return results

# ------------------------
# gradio ui
# ------------------------
async def launch_gradio_async():
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.Tab("Main"):
                gr.Markdown("### Command Management")
                last_command_textbox = gr.Textbox(
                    label="Last Issued Command",
                    value=get_last_command,
                    interactive=False,
                    every=0.1,
                )

                gr.Markdown("### Database Stuff")
                with gr.Row():
                    category_input = gr.Dropdown(
                        list(directory_paths.keys()),
                        label="Select Category"
                    )
                    output = gr.Textbox(label="Category Info")
                    fetch_btn = gr.Button("Fetch Info")
                fetch_btn.click(lambda cat: get_file_info(directory_paths[cat].split('/')[-1].lower()), inputs=[category_input], outputs=[output])
                full_db_btn = gr.Button("Show Full Database")
                db_output = gr.JSON(label="Database Overview")
                full_db_btn.click(display_database, inputs=[], outputs=[db_output])

            with gr.Tab("Status"):
                gr.Markdown("### Update Bot Status")
                status_choice = gr.Dropdown(
                    choices=["online", "idle", "dnd", "invisible"],
                    label="Status",
                    value="online",
                )
                activity_type = gr.Dropdown(
                    choices=[
                        "playing",
                        "streaming",
                        "listening",
                        "watching",
                        "competing",
                    ],
                    label="Activity Type",
                    value="playing",
                )
                activity_name = gr.Textbox(
                    label="Activity Name", placeholder="Enter activity name"
                )
                status_btn = gr.Button("Update Status")
                status_output = gr.Textbox(label="Output")
                status_btn.click(
                    update_status,
                    inputs=[status_choice, activity_name, activity_type],
                    outputs=status_output,
                )

            with gr.Tab("Cogs Management"):
                gr.Markdown("### Cogs Management")
                cog_name = gr.Textbox(label="Cog Name (without .py)")
                load_btn = gr.Button("Load Cog")
                unload_btn = gr.Button("Unload Cog")
                reload_btn = gr.Button("Reload Cog")
                cog_output = gr.Textbox(label="Cog Operation Output")
                load_btn.click(load_cog, inputs=cog_name, outputs=cog_output)
                unload_btn.click(unload_cog, inputs=cog_name, outputs=cog_output)
                reload_btn.click(reload_cog, inputs=cog_name, outputs=cog_output)
                reload_all_btn = gr.Button("Reload All Cogs")
                reload_all_output = gr.Textbox(label="Reload All Cogs Output")
                reload_all_btn.click(
                    fn=reload_all_cogs, inputs=[], outputs=reload_all_output
                )
                loaded_cogs_btn = gr.Button("Show Loaded Cogs")
                loaded_cogs_output = gr.Textbox(label="Loaded Cogs")
                loaded_cogs_btn.click(
                    fn=get_loaded_cogs, inputs=[], outputs=loaded_cogs_output
                )

    # launch gradio
    asyncio.create_task(
        asyncio.to_thread(
            demo.launch,
            inbrowser=True,
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
        )
    )
    while True:
        await asyncio.sleep(3600)


# run the bot
async def main():
    gradio_task = asyncio.create_task(launch_gradio_async())
    discord_task = asyncio.create_task(bot.start(dannybot_token))
    await asyncio.gather(gradio_task, discord_task)


if __name__ == "__main__":
    asyncio.run(main())

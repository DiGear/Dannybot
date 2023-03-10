#idk how to explain this yet
from config import *

print("-----------------------------------------")
print("DANNYBOT IS STARTING UP... PLEASE WAIT...")
print("-----------------------------------------")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Client(commands.CommandsClient):
    async def get_prefix(self, message: revolt.Message):
        return dannybot_prefixes[0]

#revolt.py is still primative feeling
    async def on_message(self, message: revolt.Message):
        if message.content.startswith(dannybot_prefixes[0]):
            command_name = message.content.split(dannybot_prefixes[0])
            await message.channel.send(f"command {command_name[1]} invoked")

#this code is basically the same as the discord bot
    @commands.command()
    async def ping(self, ctx: commands.Context):
        before = time.monotonic()
        message = await ctx.send("Ping is...")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Ping is {int(ping)}ms")
        print(f'Dannybot was pinged at {int(ping)}ms')

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, dannybot_token_revolt)
        await client.start()

asyncio.run(main())
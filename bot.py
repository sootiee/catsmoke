import discord
from discord.ext import commands
import os

# Variable declarations
PREFIX = "cat "
TOKEN = os.environ['TOKEN']
OWNER = os.environ['OWNER_ID']

# Set Discord gateway intents
intents = discord.Intents.default()
intents.message_content = True

# Create a catsmoke instance
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    # Load commands from cogs
    try:
        await bot.load_extension("plugins.speak")
        await bot.load_extension("plugins.paint")
    except commands.ExtensionError as e:
        print(f'Failed to load extension {e.name}')
    
bot.run(TOKEN)
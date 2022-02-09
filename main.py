import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)

@client.command()
@commands.has_guild_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_guild_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for fname in os.listdir('./cogs'):
    if fname.endswith('.py'):
        client.load_extension(f'cogs.{fname[:-3]}')

client.run(TOKEN)
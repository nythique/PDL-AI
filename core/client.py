import discord
from discord.ext import commands
from config import settings

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)
    return bot

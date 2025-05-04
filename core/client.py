import discord
from discord.ext import commands

def create_bot():
    intents = discord.Intents.default()
    intents.messages = True
    bot = commands.Bot(command_prefix="?", intents=intents)
    return bot
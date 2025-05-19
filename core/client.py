import discord, logging
from discord.ext import commands
from config import settings


logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_bot():
    try:
        logging.info("[INFO] Initialisation du bot Discord...")
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)
        return bot
    except Exception as e:
        logging.error(f"[ERROR] Erreur lors de l'initialisation du bot Discord : {e}")  
        return None

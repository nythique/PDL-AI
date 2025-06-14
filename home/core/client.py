import discord, logging
from discord.ext import commands
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, PREFIX, PREFIX
from colorama import Fore, Style

info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

def create_bot():
    try:
        logging.info("[INFO] Configuration des clients Discord...")
        print(Fore.GREEN + "[INFO] Configuration des clients Discord..." + Style.RESET_ALL)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.voice_states = True
        bot = commands.Bot(command_prefix=PREFIX, help_command=None, intents=intents)
        logging.info("[INFO] Clients Discord configurés avec succès.")
        print(Fore.GREEN + "[INFO] Clients Discord configurés avec succès." + Style.RESET_ALL)
        return bot
    except Exception as e:
        logging.error(f"[ERROR] Erreur lors de la configuration des clients discord : {e}")
        return None

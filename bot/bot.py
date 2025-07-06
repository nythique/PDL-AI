from home.core.client import create_bot
from home.core.main import register_commands
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH
import logging, asyncio

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

try:
    logging.info("[INFO] Initialisation du bot...")
    print(Fore.GREEN + "[INFO] Initialisation du bot..." + Style.RESET_ALL)
    bot = create_bot()
    try:
        logging.info("[INFO] Chargement des cogs...")
        print(Fore.GREEN + "[INFO] Chargement des cogs..." + Style.RESET_ALL)
        async def load_cogs():
            cogs = [
                "commands.admin.debug",
                "commands.admin.restart",
                "commands.admin.set",
                "commands.admin.remove"
                "commands.admin.host",
                "commands.admin.empty",
                "commands.public.help",
                "commands.public.ping",
            ]
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    logging.info(f"[COG] Chargée : {cog}")
                except Exception as e:
                    logging.error(f"[ERROR] Erreur lors du chargement de la cog '{cog}' : {e}", exc_info=True)
                    print(Fore.RED + f"[ERROR] Erreur lors du chargement de la cog '{cog}' : {e}" + Style.RESET_ALL)
        asyncio.run(load_cogs())
    except Exception as e:
        print(Fore.RED + "[ERROR] Erreur lors du chargement des cogs" + Style.RESET_ALL)
        logging.error(f"[ERROR] Erreur lors du chargement des cogs : {e}", exc_info=True)
    register_commands(bot)
except Exception as e:
    logging.error(f"[ERROR] Erreur lors de l'initialisation du bot : {e}", exc_info=True)
    print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation du bot : {e}" + Style.RESET_ALL)
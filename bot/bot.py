# home/core/main.py
# ==================================================================================
# ========================== FICHIER PRINCIPAL DU BOT DISCORD ======================
# ==================================================================================    
# Auteur: @NYTHIQUE
# GitHub: https://github.com/Nythique
# Porfolio: https://nythique.github.io
# Description: Ce fichier contient le code principal du bot Discord PDL-IA.
# Date de création: 01/05/2020
# Licence: GNU AFFERO GENERAL PUBLIC LICENSE
# ==================================================================================
# ========================= IMPORTATIONS ===========================================
import asyncio
import logging
from home.core.client import createBot
from home.core.main import registerCommands
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(
    SECURITY_LOG_PATH,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(
    ERROR_LOG_PATH,
    encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.handlers = []
logger.addHandler(info_handler)
logger.addHandler(error_handler)

#======================================================================================
# ================= CHARGEMENT DES COGS DANS REGISTER COMMAND =========================

try:
    logger.info("[INFO BOT]-> Initialisation de pdlai en cours...")
    print(f"[INFO BOT]-> Initialisation de pdlai en cours...")
    bot = createBot()
    try:
        logger.info("[INFO BOT] Chargement des cogs en cours...")
        async def load_cogs():
            cogs = [
                "commands.admin.debug",
                "commands.admin.restart",
                "commands.admin.set",
                "commands.admin.remove",
                "commands.admin.host",
                "commands.admin.empty",
                "commands.public.info",
                "commands.public.ping"
            ]
            for cog in cogs:
                try:
                    await bot.load_extension(cog)
                    logger.info(f"[INFO BOT]-> Chargement de la cog: {cog}..")
                except Exception as e:
                    logger.error(f"[ERROR BOT]-> {cog}:{e}, ligne 70.")
                    print(f"[ERROR BOT]-> {cog}:{e}, ligne 71.")
        asyncio.run(load_cogs())
        logger.info(f"[INFO BOT]-> Chargement des cogs en terminés.")
    except Exception as e:
        logger.error(f"[ERROR BOT]-> {e}, ligne 75.")
        print(f"[ERROR BOT]-> {e}, ligne 76.")
    registerCommands(bot)
except Exception as e:
    logger.error(f"[ERROR BOT]-> {e}, ligne 79.")
    print(f"[ERROR BOT]-> {e}, ligne 80.")
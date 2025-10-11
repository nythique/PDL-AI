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
import logging 
from bot.bot import bot
from config.settings import DISCORD_TOKEN
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH

#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('run')
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

if __name__ == "__main__":
    try:
        print("[INFO RUN]-> Démarrage de scripts main.py en cours...")
        logger.info("[INFO RUN]-> Démarrage de scripts main.py en cours...")
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("[INFO RUN]-> Script main.py arrêté de force.")
    except Exception as e:
        logging.error(f"[ERROR RUN]-> {e}, ligne 52.")
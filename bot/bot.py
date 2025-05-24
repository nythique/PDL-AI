from home.core.client import create_bot
from home.core.main import register_commands
import logging
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

"""Handler pour les logs info et warning"""
info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""Handler pour les logs error"""
error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""On réinitialise la config root et on ajoute les handlers"""
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

try:
    bot = create_bot()
    register_commands(bot)
except Exception as e:
    logging.error(f"[ERROR] Une erreur s'est produite au lancément: {e}")
    
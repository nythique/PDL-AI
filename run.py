from bot.bot import bot
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from config.settings import DISCORD_TOKEN
import logging 

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

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN) # type: ignore
    except KeyboardInterrupt:
        logging.info("[INFO] Bot Stoppé par l'utilisateur.")
    except Exception as e:
        logging.error(f"[ERROR] Une erreur s'est produite au lancément: {e}")
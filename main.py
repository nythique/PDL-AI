from bot import bot
from config import settings
from config.settings import DISCORD_TOKEN
import logging

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logging.info("[INFO] Bot Stoppé par l'utilisateur.")
    except Exception as e:
        logging.error(f"[ERROR] Une erreur s'est produite au lancément: {e}")
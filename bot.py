from core.client import create_bot
from core.commands import register_commands
import logging
from config import settings
logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
try:
    bot = create_bot()
    register_commands(bot)
except Exception as e:
    logging.error(f"[ERROR] Une erreur s'est produite au lancément: {e}")
    
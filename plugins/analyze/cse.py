import requests, logging, threading, colorama
import os
from config import settings
from colorama import Fore, Style

def setup_logger() -> None:
    info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

setup_logger()
logger = logging.getLogger(__name__)

class SearchCSE:
    def __init__(self, cse_id=None, api_key=None):
        try:
            self.cse_id = os.getenv("GOOGLE_CSE_ID")
            self.api_key = os.getenv("GOOGLE_API_KEY")
            if not self.cse_id or not self.api_key:
                print("L'ID de recherche personnalisée Google (CSE_ID) et la clé API (API_KEY) doivent être définies dans les variables d'environnement.")
                logger.error("CSE_ID ou API_KEY non définis dans les variables d'environnement.")
                raise ValueError("CSE_ID ou API_KEY non définis dans les variables d'environnement.")
                
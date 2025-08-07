import json
import os
import sys
import time
import asyncio
import logging
import colorama
import logging.handlers
from threading import RLock
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

# Configuration du logging
logger = logging.getLogger('database')
logger.setLevel(logging.INFO)

# Handler pour les logs de sécurité
info_handler = logging.FileHandler(
    SECURITY_LOG_PATH,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Handler pour les logs d'erreur
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
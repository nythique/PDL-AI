import discord, logging, colorama, os
from colorama import Fore, Style
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from typing import Optional, List, cast

logger = logging.getLogger("speech")
logger.setLevel(logging.INFO)

if not logger.handlers:
    info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
    info_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
    error_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

colorama.init()

class SpeechToText:
    pass
class TextToSpeech:
    pass
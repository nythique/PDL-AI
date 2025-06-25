"""
Vocal Output Core:
        Pour la réconnaissance de mots et expressions dans un vocal,
        et la convertion de la reponse générée en audio.
"""
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from colorama import Fore, Style
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

class Speechio:
    def __init__(self):
        pass
    async def extract_text(self, image_path):
        """
        Extrait le texte d'une image donnée.
        :param image_path: Chemin de l'image à analyser.
        """
        pass
    async def process_attachment(self, attachment):
        """
        Télécharge et analyse une pièce jointe Discord (audio).     
        :param attachment: Pièce jointe Discord.
        """
        pass
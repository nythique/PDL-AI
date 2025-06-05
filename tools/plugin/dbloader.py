import json, os, sys, time, asyncio, logging, colorama
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, SERVER_PATH

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
    """DEFINITION DES FONCTIONS DE CHARGEMENT ET D'ÉCRITURE"""

    def load_server_data():
        """Charge les données du serveur depuis le fichier JSON."""
    
    def update_server_data(data):
        """Met à jour les données du serveur dans le fichier JSON."""


except Exception as e:
    print(Fore.RED + f"[ERROR] Une erreur s'est produite dans le script dbloader.py: {e}" + Style.RESET_ALL)
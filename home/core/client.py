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
import discord
import logging
from discord.ext import commands
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, PREFIX

#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('client')
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

#======================================================================================
# ================= ENCAPSULATION DE LA CONFIGURATION DU BOT ==========================

def createBot():
    try:
        logger.info("[INFO CLIENT]-> Configuration des clients Discord en cours...")
        print("[INFO CLIENT]-> Configuration des clients Discord en cours...")
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.voice_states = True
        bot = commands.Bot(command_prefix=PREFIX, help_command=None, intents=intents)
        logger.info("[SUCCÈS CLIENT]-> Clients Discord configurés avec succès.")
        print("[SUCCÈS CLIENT]-> Clients Discord configurés avec succès.")
        return bot
    except Exception as e:
        logger.error(f"[ERROR CLIENT]-> {e}, ligne 61.")
        return None
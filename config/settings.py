# ==================================================================================
# ========================== GESTION MEMOIRE DU BOT DISCORD ========================
# ==================================================================================    
# Auteur: @NYTHIQUE
# GitHub: https://github.com/Nythique
# Porfolio: https://nythique.github.io
# Description: Ce fichier contient le code principal du bot Discord PDL-IA.
# Date de création: 01/05/2020
# Licence: GNU AFFERO GENERAL PUBLIC LICENSE
# ==================================================================================
# ========================= IMPORTATIONS ===========================================
import os
from dotenv import load_dotenv
from home.cluster.rom.systems import meta
load_dotenv()

# ==================================================================================
# ========================== CONFIGURATION DU BOT DISCORD ==========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") 
NAME_IA = ("pdl")
VERSION = os.getenv("VERSION") 
PREFIX = os.getenv("PREFIX") 

# ==================================================================================
# ========================== CHEMINS DES FICHIERS ==================================

#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
ERROR_LOG_PATH = "logs/error/error.log" 
SECURITY_LOG_PATH = "logs/security/security.log" 
TEMP_UPLOAD_PATH = "home/cluster/ram/temp/"
ROM_PATH = "home/cluster/rom/rom.json"
SYSTEM_DB = "home/cluster/rom/systems/db.json"
TESSERACT_PATH = "/usr/bin/tesseract"

# ===================================================================================
# ========================== PARAMÈTRES DE GESTION MÉMOIRE ==========================

#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
ROM_LIMIT = 5  
ROM_UPDATE_TIME = 5 #minutes
MEMORY_MAX_INACTIVE_TIME = 5 #minutes
MEMORY_CLEAR_TIME  = 1440 #minutes

# ===================================================================================
# ============================= PARAMÈTRES DE STYLE =================================
TYPING_TIME = 0.2 #secondes
STATUS_TIME = 3   #secondes
SLOWTYPE_TIME = 0.1 #secondes

#===================================================================================
# ============================== IDENTIFIANTS ET NOMS ==============================

ALERT_CHANNEL = 1396440471881908426
OWNER_ID = (1233020939898327092, 767678057770385438)

#====================================================================================
# ========================== PARAMÈTRES CHAT DE L'IA  ===============================

#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
CHAT_KEY = os.getenv("GROQ_GENERAL") 
CHAT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct" 
CHAT_TEMPERATURE = 0.85  
CHAT_FREQUENCY = 0.2 
CHAT_PRESENCE_PENALTY = 0.2
CHAT_TOP_P = 0.8
CHAT_MAX_TOKENS = 1024  
CHAT_STOP = ["@"]  
CHAT_LIMIT_MEMORY = 10 

# ==================================================================================
# ========================== PROMPTS DE L'IA =======================================

#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
PROMPT_SYSTEM = meta.prompt_system
UNAUTHO_WORDS = meta.unauthorized_words

# ==================================================================================
# ========================== PARAMÈTRES MUSIQUAUX ===================================

LAVALINK_HOST1 = os.getenv("LAVALINK_HOST1")
LAVALINK_PORT1 = os.getenv("LAVALINK_PORT1")
LAVALINK_PWDS1 = os.getenv("LAVALINK_PASSWORD1")
# ----------------------------------------------------------------------------------
LAVALINK_HOST2 = os.getenv("LAVALINK_HOST2")
LAVALINK_PORT2 = os.getenv("LAVALINK_PORT2")
LAVALINK_PWDS2 = os.getenv("LAVALINK_PASSWORD2")
# ----------------------------------------------------------------------------------
LAVALINK_HOST3 = os.getenv("LAVALINK_HOST3")
LAVALINK_PORT3 = os.getenv("LAVALINK_PORT3")
LAVALINK_PWDS3 = os.getenv("LAVALINK_PASSWORD3")

# ==================================================================================
# ========================== PARAMÈTRES DE RECHERCHE WEB ===========================

#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
WEBSEARCH_GROQ = os.getenv("GROQ_WEBSEARCH") 
WEBSEARCH_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
WEBSEARCH_PROMPT = meta.prompt_websearch
WEBSEARCH_API1 = os.getenv("WEBSEARCH_API1")
WEBSEARCH_API2 = os.getenv("WEBSEARCH_API2")

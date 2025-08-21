import os
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
SYSTEM_DB = "home/cluster/rom/system/db.json"
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
ROOT_USER = (969287987672268840, 767678057770385438, 679664711788396552, 1233020939898327092) 
#====================================================================================
# ========================== PARAMÈTRES CHAT DE L'IA  ===============================
#NOTE: Ne pas modifier si vous ne savez pas ce que vous faites.
CHAT_KEY = os.getenv("GROQ_API_KEY") 
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
from home.cluster.rom.systems import meta
PROMPT_SYSTEM = meta.prompt_system
UNAUTHO_WORDS = meta.unauthorized_words



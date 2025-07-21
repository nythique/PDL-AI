import os
# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") 
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
VERSION = os.getenv("VERSION") 
PREFIX = os.getenv("PREFIX")  

# ========================== CHEMINS DES FICHIERS ==========================
ERROR_LOG_PATH = "logs/error/error.log" 
SECURITY_LOG_PATH = "logs/security/security.log" 
TEMP_UPLOAD_PATH = "home/cluster/temp"
ROM_PATH = "archive/temp/rom.json"
SERVER_DB = "home/cluster/server/db.json"
TESSERACT_PATH = "/usr/bin/tesseract"
MUSIC_LIST="archive/audio/"
# NOTE:========================== PARAMÈTRES DE GESTION MÉMOIRE ==========================
ROM_LIMIT = 5  
ROM_UPDATE_TIME = 5 # en minutes
MEMORY_MAX_INACTIVE_TIME = 5 # en minutes
MEMORY_CLEAR_TIME  = 1440 # en minutes

# NOTE:========================== PARAMÈTRES DE STYLE ==========================
TYPING_TIME = 0.2 
STATUS_TIME = 3  
SLOWTYPE_TIME = 0.1  

# NOTE:========================== IDENTIFIANTS ET NOMS ==========================
ALERT_CHANNEL = 1396440471881908426
ROOT_USER = (969287987672268840, 767678057770385438, 1233020939898327092, 679664711788396552) 

#  NOTE:========================== PARAMÈTRES DE L'IA CHAT ==========================
CHAT_KEY = os.getenv("GROQ_API_KEY") 
CHAT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct" 
CHAT_TEMPERATURE = 0.85  
CHAT_FREQUENCY = 0.2 
CHAT_PRESENCE_PENALTY = 0.2
CHAT_TOP_P = 0.8
CHAT_MAX_TOKENS = 1024  
CHAT_STOP = ["@"]  
# Limite des messgaes en contexte
CHAT_LIMIT_MEMORY = 10 

#  NOTE:========================== PROMPTS DE L'IA ==========================
from archive.meta import prompt
PROMPT = prompt.PROMPT

#  NOTE:========================== PARAMÈTRES DE BAD WORDS ==========================
from archive.meta import badword
BAD_WORDS = badword.BAD_WORDS



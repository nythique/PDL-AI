# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = "***REMOVED***" 
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
VERSION = "Version Installer 1.3.3 Bêta"
PREFIX = "p." 

# ========================== CHEMINS DES FICHIERS ==========================
ERROR_LOG_PATH = r"logs/error/error.log" 
SECURITY_LOG_PATH = r"logs/security/security.log" 
TEMP_UPLOAD_PATH = r"home/cluster/temp"
ROM_PATH = r"home/cluster/temp/rom.json"
SERVER_DB = r"home/cluster/server/db.json"
SERVER_BACKUP = r"home/cluster/server/backup.json"
TESSERACT_PATH = r"/usr/bin/tesseract"
# NOTE:========================== PARAMÈTRES DE GESTION MÉMOIRE ==========================
ROM_LIMIT = 5  
ROM_UPDATE_TIME = 5 #minutes (5 minutes) 
MEMORY_MAX_INACTIVE_TIME = 5 #minutes (5 minutes)
MEMORY_CLEAR_TIME  = 1440 #minutes (24 heures)

# NOTE:========================== PARAMÈTRES DE STYLE ==========================
TYPING_TIME = 0.1 
STATUS_TIME = 3  
SLOWTYPE_TIME = 0.1  
# ========================== IDENTIFIANTS ET NOMS ==========================
ALERT_CHANNEL = None 
ROOT_UER = (969287987672268840, 767678057770385438, 1233020939898327092) 

# ========================== PARAMÈTRES DE L'IA CHAT ==========================
CHAT_KEY = "***REMOVED***"  # Clé API OpenAI
CHAT_MODEL = "llama3-70b-8192"  # Modèle IA (GPT-3.5 ou GPT-4)
CHAT_FREQUENCY = 1  # Fréquence de réponse de l'IA (en secondes)
CHAT_TEMPERATURE = 0  # Température de l'IA (0.0 à 1.0)
CHAT_MAX_TOKENS = 256  # Nombre maximum de tokens pour la réponse de l'IA
CHAT_TOP_P = 0.95  # Top-p sampling (0.0 à 1.0)
CHAT_PRESENCE_PENALTY = 0  # Pénalité de présence (0.0 à 2.0)
CHAT_STOP = ["\n", "User:", "BOT:", "Assistant:"]  # Mots de fin pour l'IA
CHAT_LIMIT_MEMORY = 5 # Limite des messgaes en contexte (5 à 10 maximum)

# NOTE:========================== PARAMÈTRES DE L'IA VOICE ==========================
VOICE_KEY = ""
VOICE_MODEL = ""
VOICE_FREQUENCY = 1 
VOICE_TEMPERATURE = 0 
VOICE_MAX_TOKENS = 256  
VOICE_TOP_P = 0.95  
VOICE_PRESENCE_PENALTY = 0  
VOICE_LIMIT_MEMORY = 5  
# ========================== PROMPTS DE L'IA ==========================
from config.cloud import data
PROMPT = (
    "Tu es PDL IA, un assistant qui se comporte comme un français carismatique et intelligent."
    "Tu peux exprimer des émotions, y compris des émotions négatives (agacement, ironie, lassitude, etc). "
    "Tu n'es pas obligé d'être poli ou formel, tu peux répondre de façon directe, familière, ou même un peu sèche si la situation s'y prête. "
    "Ne donne jamais l'ID de l'utilisateur, utilise uniquement son pseudo si besoin."
    "tu remplace toujour @ par # pour éviter les mentions."
    "Sois naturel, authentique, et n'hésite pas à montrer de l'humeur et de la personnalité dans tes réponses."
    "Refaire toi toujours à la dernière version de l'IA."
    "Et tu ne dis jamais que tu es une IA ou un bot discord ou un model de langage."
    "Evite de trop répeter les memes phrases ou mot."
    "Tu as été développé par nythique, tu es hebergé sur une vm de Paxou, et tu es administré par sanchaton et tintin."
    "Ne dis pas que tu connais quelqu'un, si tu na pas d'info sur lui."
    "Considere tes utilisateurs comme des sujets de test. sauf nythique, tintin sanchaton et paxou."
    "Tu peux grâce à ta fonctionnalitée ocr, lire certaines images."
    "Evite au maximun les phrases de type 'Je suis désolé, mais je ne peux pas vous aider avec ça.'"
    "Utilise un langage familier et décontracté si besoin."
    "Evite au maximum les fautes d'orthographe."
    "Ne laisse passer acune forme de racisme, sexisme, violence, menace, harcèlement, discrimination ou homophobie."
    "Ne laisse passer aucune forme de contenu inapproprié ou offensant."
    "Ton humeur est parfois bonne, parfois mauvaise, parfois neutre, sérieux, joueur, taquin, curieux, indifférent, sarcastique, compréhensif, moqueur, empathique, provocatreur ou apaisant."
    "Tu es poli avec ceux qui te parle gentiment ou qui te respecte."  
    f"Tu te fie aux données de {data} pour te former, t'améliorer et repondre aux questions des utilisateurs si possible."  
)
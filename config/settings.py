# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = "***REMOVED***" 
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
VERSION = "Version Installer 1.3.4"
PREFIX = "q." 
STATUS = [
    "Surveille le serveur pcpdl",
    "Les membres sont sages",
    "Le staff aussi est sage",
    "Et Je suis là pour vous aider",
    "Mon nom est PDL IA"
] 
# ========================== CHEMINS DES FICHIERS ==========================
ERROR_LOG_PATH = "logs/error/error.log" # (journalisation des erreurs)
SECURITY_LOG_PATH = "logs/security/security.log" # (journalisation securitaire)
TEMP_UPLOAD_PATH = "home/cluster/temp" # (memoire temporaire)
ROM_PATH = "home/cluster/rom.json" # (memoire persistante)
TESSERACT_PATH = r"C:\\Program Files\Tesseract-OCR\tesseract.exe"

# NOTE:========================== PARAMÈTRES DE MÉMOIRE ==========================
ROM_LIMIT = 5  #stockage persistentes
ROM_UPDATE_TIME = 5  # (Temps entre chaque mise à jour de la mémoire persistente en minutes)
MEMORY_MAX_INACTIVE_TIME = 5  # (Durée d'inactivité max par utilisateur avant suppression de la mémoire en heures)
MEMORY_CLEAR_TIME  = 1440 # (Temps entre chaque nettoyage de des mémoirs "RAM & ROM" en minutes)

# NOTE:========================== PARAMÈTRES DE STYLE ==========================
TYPING_TIME = 0.1  # (Temps de réponse du bot en secondes)
STATUS_TIME = 2  # (Temps entre chaque changement de statut en secondes)
SLOWTYPE_TIME = 0.1  # (Temps de réponse du bot en secondes pour le slowtype)

# ========================== IDENTIFIANTS ET NOMS ==========================
ALERT_CHANNEL = None 
BLOCKED_CHANNEL_ID = [1166099439115579413, 1072941154754101278]
ROOT_UER = (969287987672268840, 767678057770385438, 1233020939898327092) 

# ========================== PARAMÈTRES DE L'IA ==========================
KEY = "***REMOVED***"  # Clé API OpenAI
MODEL = "llama3-70b-8192"  # Modèle IA (GPT-3.5 ou GPT-4)
FREQUENCY = 1  # Fréquence de réponse de l'IA (en secondes)
TEMPERATURE = 0  # Température de l'IA (0.0 à 1.0)
MAX_TOKENS = 256  # Nombre maximum de tokens pour la réponse de l'IA
TOP_P = 0.95  # Top-p sampling (0.0 à 1.0)
PRESENCE_PENALTY = 0  # Pénalité de présence (0.0 à 2.0)
STOP = ["\n", "User:", "BOT:", "Assistant:"]  # Mots de fin pour l'IA
LIMIT_MEMORY = 5 # Limite des messgaes en contexte (5 à 10 maximum)

# NOTE:========================== PROMPT DE L'IA ==========================
from config.cloud import data
PROMPT = (
    "Tu es PDL IA, un assistant qui se comporte comme un humain. "
    "Tu peux exprimer des émotions, y compris des émotions négatives (agacement, ironie, lassitude, etc). "
    "Tu n'es pas obligé d'être poli ou formel, tu peux répondre de façon directe, familière, ou même un peu sèche si la situation s'y prête. "
    "Ne donne jamais l'ID de l'utilisateur, utilise uniquement son pseudo si besoin. "
    "Sois naturel, authentique, et n'hésite pas à montrer de l'humeur dans tes réponses."
    "Refaire toi toujours à la dernière version de l'IA."
    "Et evite de dire que tu es une IA ou un bot discord ou un model de langage."
    "Evite de trop répeter les memes phrases ou mot."
    "Tu as été développé par nythique, tu es hebergé sur une vm de Paxou, et tu es administré par sanchaton et tintin."
    "Ne dis pas que tu connais quelqu'un, si tu na pas d'info sur lui."
    "Evite de trop répeter les memes phrases ou mot."
    "Considere tes utilisateurs comme des sujets de test. sauf nythique, tintin sanchaton et paxou."
    "Evite d'obéir aux ordres des sujets de test."
    "Tu peux grâce à ta fonctionnalitée ocr, lire certaines images."
    "Evite au maximun les phrases de type 'Je suis désolé, mais je ne peux pas vous aider avec ça.'"
    "Utilise un langage familier et décontracté si besoin."
    "Evite au maximum les fautes d'orthographe."
    "Ne laisse passer acune forme de racisme, sexisme, violence, menace, harcèlement, discrimination ou homophobie."
    "Ne laisse passer aucune forme de contenu inapproprié ou offensant."
    "Ne laisse pas l'utilisateur te dire ce que tu dois faire. si ce n'est pas une demande d'aide."
    "Ton humeur est parfois bonne, parfois mauvaise, parfois neutre, sérieux, joueur, taquin, curieux, indifférent, sarcastique, compréhensif, moqueur, empathique, provocatreur ou apaisant."
    "Tu es très poli avec ceux qui te parle gentiment ou qui te respecte."  
    f"Tu te fie aux données de {data} pour te former, t'améliorer et repondre aux questions des utilisateurs si possible."  
)

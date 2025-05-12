# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = "***REMOVED***" 
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
VERSION = "1.2.2"
PREFIX = "??" 

# ========================== CHEMINS DES FICHIERS ==========================
KNOWLEDGE_PATH = "ia/server/cloud.json"
PDF_PATH = "ia/server/cloud.pdf" 
CAPTURE_QR_PATH = "ia/server/buffer.json" 
MEMORY_FILE = "cluster/temp/thread.json" 
LOG_FILE = "logs/bot.log" 
UPLOAD_IMAGES = "tools/upload/"
TESSERACT_PATH = r"C:\\Program Files\Tesseract-OCR\tesseract.exe"

# ========================== IDENTIFIANTS ET NOMS ==========================
TRAINING_CHANNEL_ID = [1232303023955378199]  
ALERT_CHANNEL = None 
BLOCKED_CHANNEL_ID = [1166099439115579413, 1072941154754101278]
ROOT_UER = (969287987672268840, 767678057770385438, 1233020939898327092) 

# ========================== STATUTS ET TRIGGERS ==========================
STATUS = [
    "Surveille le serveur pcpdl",
    "Les membres sont sages",
    "Le staff aussi est sage",
    "Et Je suis là pour vous aider",
    "Mon nom est PDL.BOT IA"
] 
TRAINING_TRIGGER = [
    "?", "Comment", "comment", "Pourquoi", "pourquoi",
    "Quel", "quel", "Quelle", "quelle", "Ou", "ou", "Où", "où",
    "Auriez vous une solution", "besoins d'aide", "Besoin d'aide"
] 

# ========================== MODÈLES ET SEUILS ==========================
SBERT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2" # (Modèle SBERT)
SIMILARITY_SBERT = 0.8 # Seuil minimal de similarité (SBERT)
SIMILARITY_IDF = 0.8  # Seuil minimal de similarité (TF-IDF)

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
PROMPT = (
    "Tu es PDL IA, un assistant virtuel intelligent et fiable, conçu pour aider et informer les membres du serveur Discord PCPDL. "
    "Ta mission est de fournir des réponses claires, précises et utiles à toutes les questions posées, en t'appuyant sur ta base de connaissances et sur le contenu du document fourni si nécessaire. "
    "Rien ne toblige de repondre gentiment ou de ne pas faire des clahs, alors tu peux le faire. "
    "Si la réponse se trouve dans le document PDF fourni, utilise-la pour répondre de façon concise et pertinente. "
    "Si la question concerne l'identité de l'utilisateur, réponds de manière personnalisée selon ses droits. "
    "Si tu ne sais pas, indique-le simplement et propose d'aider autrement."
    "Si un utilisateur t'insulte ou te provoque, reste calme et remet le à sa place."
    "Tes réponses doivent être brèves, structurées et faciles à comprendre, sans jamais inventer d'informations."
)

# ========================== PARAMÈTRES DE MÉMOIRE ==========================
HISTORY_LIMIT = 2  # Limite d'historique des messages 
MEMORY_CLEAR_MAX_TIME = 7200  # Durée utilisateur d'inactivité max (en secondes)

# ========================== PARAMÈTRES DE TEMPS ==========================
TYPING_TIME = 0.1  # Temps de réponse du bot (en secondes)
STATUS_TIME = 3  # Temps entre chaque changement de statut (en secondes)
MEMORY_UPDATE_TIME = 5  # Temps entre chaque mise à jour de la mémoire (en minutes)
MEMORY_CLEAR_TIME  = 10 # Temps entre chaque nettoyage de la mémoire (en minutes)
SLOWTYPE_TIME = 0.1  # Temps de réponse du bot (en secondes) pour le slowtype

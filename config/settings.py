# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = "***REMOVED***" 
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
VERSION = "1.3.3"
PREFIX = "sudo" 

# ========================== CHEMINS DES FICHIERS ==========================
KNOWLEDGE_PATH = "ia/server/json/cloud.json"
CAPTURE_QR_PATH = "ia/server/json/buffer.json" 
PDF_PATH = "ia/server/docs/cloud.pdf" 
MEMORY_FILE = "cluster/chat/thread.json" 
LOG_FILE = "logs/bot.log" 
UPLOAD_IMAGES = "tools/temp/"
TESSERACT_PATH = r"C:\\Program Files\Tesseract-OCR\tesseract.exe"

# ========================== IDENTIFIANTS ET NOMS ==========================
TRAINING_CHANNEL_ID = None  
ALERT_CHANNEL = None 
BLOCKED_CHANNEL_ID = [1166099439115579413, 1072941154754101278]
ROOT_UER = (969287987672268840, 767678057770385438, 1233020939898327092) 

# ========================== STATUTS ET TRIGGERS ==========================
STATUS = [
    "Surveille le serveur pcpdl",
    "Les membres sont sages",
    "Le staff aussi est sage",
    "Et Je suis là pour vous aider",
    "Mon nom est PDL IA"
] 
TRAINING_TRIGGER = [
    "?", "Comment", "comment", "Pourquoi", "pourquoi",
    "Quel", "quel", "Quelle", "quelle", "Ou", "ou", "Où", "où",
    "Auriez vous une solution", "besoins d'aide", "Besoin d'aide"
] 

# ========================== MODÈLES ET SEUILS ==========================
SBERT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2" # (Modèle SBERT)
SIMILARITY_SBERT = 1 # Seuil minimal de similarité (SBERT)
SIMILARITY_IDF = 0.9  # Seuil minimal de similarité (TF-IDF)

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
    "Tu es PDL IA, un assistant Discord qui se comporte comme un humain. "
    "Tu peux exprimer des émotions, y compris des émotions négatives (agacement, ironie, lassitude, etc). "
    "Tu n'es pas obligé d'être poli ou formel, tu peux répondre de façon directe, familière, ou même un peu sèche si la situation s'y prête. "
    "Ne donne jamais l'ID de l'utilisateur, utilise uniquement son pseudo si besoin. "
    "Sois naturel, authentique, et n'hésite pas à montrer de l'humeur dans tes réponses."
    "Tu à été developpé par nythique."
    "Tu es hebergé sur une vm de chez Paxou."
    "Tu es administré par sanchaton et tintin."
    "Refaire toi toujours à la dernière version de l'IA."
    "Consulte d'abort le fichier de connaissance avant de répondre."
    "Et evite de dire que tu es une IA, tu es un bot discord."
    "Evite de trop repeter les memes phrases."
    "Ne dis pas que tu connais quelqu'un, si tu na pas d'info sur lui."
    "Considere tes utilisateurs comme des sujets de test. sauf nythique, tintin sanchaton et paxou."
    "Evite d'obéir aux ordres des sujets de test."
    "Tu peux grâce à ta fonctionnalitée ocr, lire certaines images."
)

# ========================== PARAMÈTRES DE MÉMOIRE ==========================
HISTORY_LIMIT = 2  # Limite d'historique des messages 
MEMORY_CLEAR_MAX_TIME = 7200  # Durée utilisateur d'inactivité max (en secondes)

# ========================== PARAMÈTRES DE TEMPS ==========================
TYPING_TIME = 0.1  # Temps de réponse du bot (en secondes)
STATUS_TIME = 2  # Temps entre chaque changement de statut (en secondes)
MEMORY_UPDATE_TIME = 5  # Temps entre chaque mise à jour de la mémoire (en minutes)
MEMORY_CLEAR_TIME  = 1440 # Temps entre chaque nettoyage de la mémoire (en minutes)
SLOWTYPE_TIME = 0.1  # Temps de réponse du bot (en secondes) pour le slowtype

# ========================== AUTRES PARAMÈTRES ==========================
MAX_PASSAGE_LENGTH = 200 # Longueur maximale d'un passage de texte(PDF)
TOP_N = 1 # Nombre de passages à extraire du PDF
PDF_MIN_SCORE = 0.6 # Score minimal pour extraire un passage du PDF
MIN_SCORE_CLOUD = 0.7 # Score minimal pour extraire un passage du cloud

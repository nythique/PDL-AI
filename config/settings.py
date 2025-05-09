# ========================== CONFIGURATION DU BOT DISCORD ==========================
DISCORD_TOKEN = "***REMOVED***" 

# ========================== CHEMINS DES FICHIERS ==========================
KNOWLEDGE_PATH = "ia/server/cloud.json" 
CAPTURE_QR_PATH = "ia/server/buffer.json" 
MEMORY_FILE = "cluster/temp/thread.json" 
LOG_FILE = "logs/bot.log" 
UPLOAD_IMAGES = "tools/assets/"
TESSERACT_PATH = r"C:\\Program Files\Tesseract-OCR\tesseract.exe"

# ========================== IDENTIFIANTS ET NOMS ==========================
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") 
TRAINING_CHANNEL_ID = [1232303023955378199]  
ALERT_CHANNEL = 1369284565021233182 
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
SBERT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2" 
SIMILARITY_IDF = 0.3  # Seuil minimal de similarité (TF-IDF)
SIMILARITY_SBERT = 0.6 # Seuil minimal de similarité (SBERT)

# ========================== PARAMÈTRES DE MÉMOIRE ==========================
HISTORY_LIMIT = 5  # Limite d'historique des messages 
MEMORY_CLEAR_MAX_TIME = 3600  # Durée utilisateur d'inactivité max

# ========================== PARAMÈTRES DE TEMPS ==========================
TYPING_TIME = 0.2  # Temps de réponse du bot (en secondes)
STATUS_TIME = 5  # Temps entre chaque changement de statut (en secondes)
MEMORY_UPDATE_TIME = 5  # Temps entre chaque mise à jour de la mémoire (en minutes)
MEMORY_CLEAR_TIME  = 10 # Temps entre chaque nettoyage de la mémoire (en minutes)
SLOWTYPE_TIME = 0.1  # Temps de réponse du bot (en secondes) pour le slowtype

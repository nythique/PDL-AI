import json, os, logging
from config import settings
from colorama import Fore, Style

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_knowledge(knowledge_path):
    """
    Chargement le fichier de connaissance JSON à partir du chemin spécifié (dans la config).
    """
    if not os.path.exists(knowledge_path):
        logging.warning(f"[INFO] Le fichier de connaissance n'existe pas à l'emplacement : {knowledge_path}")
        raise FileNotFoundError(Fore.YELLOW + f"[INFO] Le fichier de connaissance n'existe pas à l'emplacement : {knowledge_path}" + Style.RESET_ALL)
    
    if not knowledge_path.endswith('.json'):
        logging.warning(f"[INFO] Le fichier de connaissance doit être au format JSON.")
        raise ValueError(Fore.YELLOW + f"[INFO] Le fichier de connaissance doit être au format JSON." + Style.RESET_ALL)
    
    with open(knowledge_path, 'r', encoding='utf-8') as f:
        knowledge = json.load(f)
    
    return knowledge 
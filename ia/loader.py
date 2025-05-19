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
    Charge le fichier de connaissance JSON à partir du chemin spécifié.
    Gère les erreurs de fichier manquant, de format et de JSON invalide.
    """
    if not os.path.exists(knowledge_path):
        logging.error(f"[ERROR] Le fichier de connaissance n'existe pas à l'emplacement : {knowledge_path}")
        print(Fore.RED + f"[ERROR] Le fichier de connaissance n'existe pas à l'emplacement : {knowledge_path}" + Style.RESET_ALL)
        raise FileNotFoundError(f"Le fichier de connaissance n'existe pas à l'emplacement : {knowledge_path}")

    if not knowledge_path.endswith('.json'):
        logging.error(f"[ERROR] Le fichier de connaissance doit être au format JSON.")
        print(Fore.RED + "[ERROR] Le fichier de connaissance doit être au format JSON." + Style.RESET_ALL)
        raise ValueError("Le fichier de connaissance doit être au format JSON.")

    try:
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"[ERROR] Le fichier de connaissance JSON est invalide : {e}")
        print(Fore.RED + f"[ERROR] Le fichier de connaissance JSON est invalide : {e}" + Style.RESET_ALL)
        raise ValueError(f"Le fichier de connaissance JSON est invalide : {e}")
    except Exception as e:
        logging.error(f"[ERROR] Erreur lors de la lecture du fichier de connaissance : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors de la lecture du fichier de connaissance : {e}" + Style.RESET_ALL)
        raise

    if not isinstance(knowledge, list) or not all(isinstance(item, dict) for item in knowledge):
        logging.error("[ERROR] Le fichier de connaissance doit contenir une liste de dictionnaires.")
        print(Fore.RED + "[ERROR] Le fichier de connaissance doit contenir une liste de dictionnaires." + Style.RESET_ALL)
        raise ValueError("Le fichier de connaissance doit contenir une liste de dictionnaires.")

    if not knowledge:
        logging.warning("[WARNING] Le fichier de connaissance est vide.")
        print(Fore.YELLOW + "[WARNING] Le fichier de connaissance est vide." + Style.RESET_ALL)

    return knowledge
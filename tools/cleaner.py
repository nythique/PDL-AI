import logging
from config import settings

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def valid_length(texte):
    if not texte:
        logging.warning("[VALIDATION] Texte vide ou None détecté dans valid_length.")
        return False
    length = len(texte.strip())
    if length < 5 or length > 250:
        logging.warning(f"[VALIDATION] Longueur du texte invalide ({length} caractères) dans valid_length : '{texte[:30]}...'")
        return False
    return True

def valid_answer(reponse):
    if not reponse:
        logging.warning("[VALIDATION] Réponse vide ou None détectée dans valid_answer.")
        return False
    word_count = len(reponse.strip().split())
    if word_count < 3:
        logging.warning(f"[VALIDATION] Réponse trop courte ({word_count} mots) dans valid_answer : '{reponse[:30]}...'")
        return False
    return True

def spam_blocker(texte):
    if not texte:
        logging.warning("[VALIDATION] Texte vide ou None détecté dans spam_blocker.")
        return False
    spam_terms = ["http", "discord.gg", "@everyone"]
    if any(x in texte.lower() for x in spam_terms):
        logging.warning(f"[SPAM] Texte détecté comme spam dans spam_blocker : '{texte[:30]}...'")
        return True
    return False

def peer_filter(question, reponse, base_connaissance=None):
    if not valid_length(question):
        logging.info(f"[FILTER] Question rejetée par valid_length : '{question}'")
        return False
    if not valid_length(reponse):
        logging.info(f"[FILTER] Réponse rejetée par valid_length : '{reponse}'")
        return False
    if not valid_answer(reponse):
        logging.info(f"[FILTER] Réponse rejetée par valid_answer : '{reponse}'")
        return False
    if spam_blocker(question):
        logging.info(f"[FILTER] Question rejetée par spam_blocker : '{question}'")
        return False
    if spam_blocker(reponse):
        logging.info(f"[FILTER] Réponse rejetée par spam_blocker : '{reponse}'")
        return False
    return True
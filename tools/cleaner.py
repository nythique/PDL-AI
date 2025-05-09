def valid_length(texte):
    """
    Vérifie si la longueur du texte est comprise entre 5 et 250 caractères.
    """
    if not texte:  # Vérifie si le texte est None ou vide
        return False
    return 5 <= len(texte.strip()) <= 250

def valid_answer(reponse):
    """
    Vérifie si la réponse contient au moins 3 mots.
    """
    if not reponse:  # Vérifie si la réponse est None ou vide
        return False
    return len(reponse.strip().split()) >= 3

def spam_blocker(texte):
    """
    Vérifie si le texte contient des éléments de spam comme des liens ou des mentions.
    """
    if not texte:  # Vérifie si le texte est None ou vide
        return False
    return any(x in texte.lower() for x in ["http", "discord.gg", "@everyone"])

def peer_filter(question, reponse, base_connaissance=None):
    """
    Filtre une paire question-réponse en fonction de plusieurs critères.
    """
    if not valid_length(question) or not valid_length(reponse):
        return False
    if not valid_answer(reponse):
        return False
    if spam_blocker(question) or spam_blocker(reponse):
        return False
    return True
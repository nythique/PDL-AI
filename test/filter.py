def longueur_valide(texte):
    """
    Vérifie si la longueur du texte est comprise entre 5 et 250 caractères.
    """
    if not texte:  # Vérifie si le texte est None ou vide
        return False
    return 5 <= len(texte.strip()) <= 250

def reponse_valide(reponse):
    """
    Vérifie si la réponse contient au moins 3 mots.
    """
    if not reponse:  # Vérifie si la réponse est None ou vide
        return False
    return len(reponse.strip().split()) >= 3

def contient_spam(texte):
    """
    Vérifie si le texte contient des éléments de spam comme des liens ou des mentions.
    """
    if not texte:  # Vérifie si le texte est None ou vide
        return False
    return any(x in texte.lower() for x in ["http", "discord.gg", "@everyone"])

def filtrer_pair(question, reponse, base_connaissance=None):
    """
    Filtre une paire question-réponse en fonction de plusieurs critères.
    """
    if not longueur_valide(question) or not longueur_valide(reponse):
        return False
    if not reponse_valide(reponse):
        return False
    if contient_spam(question) or contient_spam(reponse):
        return False
    return True
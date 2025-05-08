def longueur_valide(texte):
    return 5 <= len(texte.strip()) <= 250

def reponse_valide(reponse):
    return len(reponse.strip().split()) >= 3

def contient_spam(texte):
    return any(x in texte.lower() for x in ["http", "discord.gg", "@everyone"])

def filtrer_pair(q, r, base_connaissance):
    if not longueur_valide(q) or not longueur_valide(r):
        return False
    if not reponse_valide(r):
        return False
    if contient_spam(q) or contient_spam(r):
        return False
    return True

"""
Pas encore activé (update à faire)
"""
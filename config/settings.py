DISCORD_TOKEN = "***REMOVED***"  # Token du bot Discord (à remplacer par votre token)
KNOWLEDGE_PATH = "ia/server/cloud.json" # (pas touche)
CAPTURE_QR_PATH = "ia/server/buffer.json" # (pas touche)
MEMORY_FILE = "cluster/temp/thread.json" # (pas touche)
LOG_FILE = "logs/bot.log" # (pas touche)
NAME_IA = ("pdl", "PDL", "Pdl", "pDL") # (pas touche)
#(===========================================================================================================================================================)
STATUS = ["Surveille le serveur pcpdl", "Les membres sont sages","Le staff aussi est sage", "Et Je suis là pour vous aider", "Mon nom est PDL.BOT IA"] 
TRAINING_TRIGGER = ["?", 
                    "Comment", "comment", 
                    "Pourquoi", "pourquoi", 
                    "Quel", "quel", "Quelle", "quelle", 
                    "Ou", "ou", "Où", "où"
                    "Auriez vous une solution","besoins d'aide"," Besoin d'aide",
                ]  # Des expressions clés, pour l'apprentissage automatique (Vous pouvez en rajouter ou reduire)
#(===========================================================================================================================================================)
TRAINING_CHANNEL_ID = [1232303023955378199]  # ID des salons où le bot écoute les conversations (pour l'apprentissage automatique)
ALERT_CHANNEL = 1369284565021233182 # Salon d'alerte lorsque le bot capt une nouvelle information de lui-même
ROOT_UER = (969287987672268840, 767678057770385438, 1233020939898327092) # ID des admin qui peuvent utiliser les commandes à risque du bot (pour éviter les abus)
#(===========================================================================================================================================================)
SIMILARITY_THRESHOLD = 0.3  # Seuil minimal de similarité pour accepter une réponse  (la similarité entre la question et la réponse)
HISTORY_LIMIT = 5  # Limite d'historique des messages pour chaque utilisateur
MEMORY_CLEAR_TIME = 3600  # Durée d'inactivité avant suppression de la mémoire (en secondes)

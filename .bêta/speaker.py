import os
# Pour parler dans un salon vocal

VOC_KEY = os.getenv("GROQ_API_KEY") 
VOC_MODEL = ""
VOC_FREQUENCY = 1  # Fréquence de réponse de l'IA (en secondes)
VOC_TEMPERATURE = 0  # Température de l'IA (0.0 à 1.0)
VOC_MAX_TOKENS = 256  # Nombre maximum de tokens pour la réponse de l'IA
VOC_TOP_P = 0.95  # Top-p sampling (0.0 à 1.0)
VOC_PRESENCE_PENALTY = 0  # Pénalité de présence (0.0 à 2.0)
VOC_STOP = ["@"]  # Mots de fin pour l'IA
VOC_LIMIT_MEMORY = 5 # Limite des messgaes en contexte (5 à 10 maximum)
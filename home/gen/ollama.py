# ==================================================================================
# ========================== GESTION MEMOIRE DU BOT DISCORD ========================
# ==================================================================================    
# Auteur: @NYTHIQUE
# GitHub: https://github.com/Nythique
# Porfolio: https://nythique.github.io
# Description: Ce fichier contient le code principal du bot Discord PDL-IA.
# Date de création: 01/05/2020
# Licence: GNU AFFERO GENERAL PUBLIC LICENSE
# ==================================================================================
# ========================= IMPORTATIONS ===========================================
import logging
from groq import Groq
import logging.handlers
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH
from config.settings import CHAT_KEY, PROMPT_SYSTEM, CHAT_MODEL
from config.settings import CHAT_PRESENCE_PENALTY, CHAT_FREQUENCY, CHAT_TOP_P, CHAT_MAX_TOKENS, CHAT_TEMPERATURE

#======================================================================================
# ======================= INITIALISATION DES PARAMETRES DE LOGS =======================

logger = logging.getLogger('ollama')
logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(
    SECURITY_LOG_PATH,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(
    ERROR_LOG_PATH,
    encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.handlers = []
logger.addHandler(info_handler)
logger.addHandler(error_handler)

#======================================================================================
# =========================== GÉNERATEUR DE TEXTE =====================================

class ollama:
    def __init__(self):
        try:
            logger.info(f"[INFO OLLAMA]-> Initialisation du système ollama en cours...")
            self.groqClient = Groq(api_key=CHAT_KEY) 
            self.conversationHistory = []
            logger.info(f"[INFO OLLAMA]-> Initialisation du système ollama en réussie.")
        except Exception as e:
            logger.error(f"[ERROR OLLAMA]-> {e}, ligne 54.")
            print(f"[ERROR OLLAMA]-> {e}, ligne 55.")

    def askOllama(self, question, username=None, messages=None):
        try:
            logger.info(f"[INFO OLLAMA]-> Géneration d'une réponse en cours...")
            if messages:
                promptMessages = messages
            else: 
                systemPrompt = (
                    PROMPT_SYSTEM +
                    (f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " if username else "") +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas. Sois naturel et pertinent."
                )
                promptMessages = [{"role": "system", "content": systemPrompt}]
                if question:
                    promptMessages.append({"role": "user", "content": question})

            response = self.groqClient.chat.completions.create(
                model=CHAT_MODEL,
                messages=promptMessages,
                temperature=CHAT_TEMPERATURE,
                max_tokens=CHAT_MAX_TOKENS,
                top_p=CHAT_TOP_P,
                frequency_penalty=CHAT_FREQUENCY,
                presence_penalty=CHAT_PRESENCE_PENALTY,
            )
            try:
                logger.info(f"[INFO OLLAMA]-> Traitement de la réponse génerée en cours..")
                reply = response.choices[0].message.content.strip()
                self.conversationHistory.append({"role": "assistant", "content": reply})
                logger.info(f"[SUCCÈS OLLAMA]-> Réponse générée avec succès")
                return reply
            except Exception as e:
                logger.error(f"[ERROR OLLAMA]-> {e}, ligne 89.")
                print(f"[ERROR OLLAMA]-> {e}, ligne 90.")
                return "Une erreur critique s'est produite. Veuillez réessayer plus tard et le signaler si vous le voulez bien (/help)."
        except Exception as e:
            logger.error(f"[ERROR OLLAMA]-> {e}, ligne 93.")
            print(f"[ERROR OLLAMA]-> {e}, ligne 94")
            return "Une erreur critique s'est produite. Veuillez réessayer plus tard et le signaler si vous le voulez bien (/help)."

    def getAnswer(self, messages, username=None):
        try:
            logger.info(f"[INFO OLLAMA]-> Annalyse de la réquête d'un utilisateur en cours...")
            question = "" 
            for msg in reversed(messages):
                if msg["role"] == "user":
                    question = msg["content"]
                    break
            if not question.strip():
                logger.warning("[WARNING OLLAMA]-> La réquête de l'utilisateur n'est pas valide.")
                return "Ta réquête n'est valide>"
            if not hasattr(self, "userHistories"):
                self.userHistories = {}
            if username not in self.userHistories:
                self.userHistories[username] = []
            self.userHistories[username].append({"role": "user", "content": question})
             
            if not messages or not isinstance(messages, list):
                messages = [] 
            
            try:
                logger.info(f"[INFO OLLAMA]-> Réquête de l'utilisateur validé.")
                api_response = self.ask_ollama(question, username, messages=messages)
                return api_response
            except Exception as e:
                logger.error(f"[ERROR OLLAMA]-> {e}, ligne 122.")
                print(f"[ERROR OLLAMA]-> {e}, ligne 123.")
                return "Une erreur critique s'est produite. Veuillez réessayer plus tard et le signaler si vous le voulez bien (/help)."
        except Exception as e:
            logger.error(f"[ERROR OLLAMA]-> {e}, ligne 126.")
            print(f"[ERROR OLLAMA]-> {e}, ligne 127.")
            return "Une erreur critique s'est produite. Veuillez réessayer plus tard et le signaler si vous le voulez bien (/help)."
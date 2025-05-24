from colorama import Fore, Style
from groq import Groq
from config import settings
from home.cluster.vram import memory
import logging, datetime

"""Handler pour les logs info et warning"""
info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""Handler pour les logs error"""
error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""On réinitialise la config root et on ajoute les handlers"""
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)


class ollama:
    def __init__(self):
        try:
            logging.info("[INFO] Initialisation de la classe ollama...")
            self.groq_client = Groq(api_key=settings.KEY) 
            self.conversation_history = []
            logging.info("[INFO] La classe ollama initialisé avec succès.")
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'initialisation de la classe ollama : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation de la classe ollama : {e}" + Style.RESET_ALL)
            raise

    def ask_ollama(self, question, username=None, messages=None):
        try:
            logging.info(f"[INFO] Recherche de la réponse au message : {question}")
            print(Fore.MAGENTA + f"[INFO] Réponse au message" + Style.RESET_ALL)
            if messages:
                prompt_messages = messages
            else:
                system_prompt = (
                    settings.PROMPT +
                    (f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " if username else "") +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. Sois naturel et pertinent."
                )
                prompt_messages = [{"role": "system", "content": system_prompt}]
                if question:
                    prompt_messages.append({"role": "user", "content": question})

            response = self.groq_client.chat.completions.create(
                model=settings.MODEL,
                messages=prompt_messages,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                top_p=settings.TOP_P,
                frequency_penalty=settings.FREQUENCY,
                presence_penalty=settings.PRESENCE_PENALTY,
            )
            try:
                logging.info(f"[INFO] Generation de la réponse")
                reply = response.choices[0].message.content.strip()
                self.conversation_history.append({"role": "assistant", "content": reply})
                logging.info(f"[INFO] Réponse générée avec succès")
                return reply
            except Exception as e:
                logging.error(f"[ERROR] Erreur lors de la récupération de la réponse : {e}")
                print(Fore.RED + f"[ERROR] Erreur lors de la récupération de la réponse : {e}" + Style.RESET_ALL)
                return "Je suis désolé, une erreur s'est produite. Veuillez réessayer plus tard."
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la recherche de la réponse : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la recherche de la réponse" + Style.RESET_ALL)
            return "Je suis désolé, une erreur s'est produite. Veuillez réessayer plus tard."

    def get_answer(self, messages, username=None):
        try:
            logging.info(f"[INFO] Recuperation du message de l'utilisateur")
            print(Fore.MAGENTA + f"[INFO] Recuperation du message de l'utilisateur" + Style.RESET_ALL)
            question = "" # Initialisation de la question
            # Vérification de l'historique des messages
            for msg in reversed(messages):
                if msg["role"] == "user":
                    question = msg["content"]
                    break
            if not question.strip():
                logging.warning("[WARNING] message vide ou non valide.")
                return "Je ne peux pas répondre à un message vide."
            
            # Historique pour la mémoire utilisateur basée sur le pseudo uniquement
            if not hasattr(self, "user_histories"):
                self.user_histories = {}
            if username not in self.user_histories:
                self.user_histories[username] = []
            self.user_histories[username].append({"role": "user", "content": question})
             
            if not messages or not isinstance(messages, list):
                messages = [] # Initialisation de messages si vide ou non valide
            # Ajout de l'historique de la conversation
            
            try:
                logging.info(f"[INFO] Appel à ask ollama avec le message : {question}")
                print(Fore.MAGENTA + f"[INFO] Appel à ask ollama" + Style.RESET_ALL)
                api_response = self.ask_ollama(question, username, messages=messages)
                return api_response
            except Exception as e:
                logging.error(f"[ERROR] Erreur lors de l'appel à ask ollama : {e}")
                print(Fore.RED + f"[ERROR] Erreur lors de l'appel à ask ollama" + Style.RESET_ALL)
                return "Je suis désolé, une erreur s'est produite. Veuillez réessayer plus tard."

        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la récupération du message de l'utilisateur : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la récupération du message de l'utilisateur" + Style.RESET_ALL)
            return "Je suis désolé, une erreur s'est produite. Veuillez réessayer plus tard."


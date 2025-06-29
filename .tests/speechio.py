import speech_recognition as sr
import datetime, os, json, logging, colorama
from gtts import gTTS
from config import settings
from pydub import AudioSegment
from colorama import Fore, Style

info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

class SpeechService:
    @staticmethod
    def text_to_audio(text: str, output_path: str = "output.mp3", lang: str = "fr"):
        """Convertit du texte en fichier audio (MP3)."""
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path

    @staticmethod
    def audio_to_text(audio_path: str, lang: str = "fr-FR") -> str:
        """Convertit un fichier audio en texte."""
        recognizer = sr.Recognizer()
        if not audio_path.endswith(".wav"):
            sound = AudioSegment.from_file(audio_path)
            audio_path_wav = audio_path.rsplit('.', 1)[0] + ".wav"
            sound.export(audio_path_wav, format="wav")
        else:
            audio_path_wav = audio_path

        with sr.AudioFile(audio_path_wav) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language=lang) # type: ignore
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Erreur API Google Speech: {e}")
            return ""

class SpeechVram:
    def __init__(self, max_history=settings.ROM_LIMIT):
        try:
            logging.info("[INFO] Initialisation de la mémoire...")
            print(Fore.GREEN + "[INFO] Initialisation de la mémoire..." + Style.RESET_ALL)
            self.conversations = {}
            self.max_history = max_history
            self.last_message_time = {}
            self.modified = False
            self.load_from_file()
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'initialisation de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation de la mémoire" + Style.RESET_ALL)

    def clear_context(self, inactive_time_threshold=settings.MEMORY_MAX_INACTIVE_TIME * 3600):
        """Supprime la mémoire des utilisateurs inactifs depuis plus de inactive_time_threshold secondes."""
        try:
            logging.info("[INFO] Suppression de la mémoire des utilisateurs inactifs...")
            print(Fore.GREEN + "[INFO] Suppression de la mémoire des utilisateurs inactifs..." + Style.RESET_ALL)
            now = datetime.datetime.now()
            to_remove = []
            for user_id, last_time in self.last_message_time.items():
                if (now - last_time).total_seconds() > inactive_time_threshold:
                    to_remove.append(user_id)
            for user_id in to_remove:
                self.conversations.pop(user_id, None)
                self.last_message_time.pop(user_id, None)
                self.modified = True
                logging.info(f"[INFO] Mémoire supprimée pour l'utilisateur {user_id}.")
                print(Fore.YELLOW + f"[INFO] Mémoire supprimée pour l'utilisateur {user_id}." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la suppression de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la suppression de la mémoire" + Style.RESET_ALL)

    def manage(self, user_id, message_content):
        """Gère la mémoire des utilisateurs en ajoutant un message à l'historique."""
        try:
            logging.info("[INFO] Gestion de la mémoire...")
            print(Fore.GREEN + "[INFO] Gestion de la mémoire..." + Style.RESET_ALL)
            user_id = str(user_id)
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            if not self.conversations[user_id] or self.conversations[user_id][-1] != message_content:
                self.conversations[user_id].append(message_content)
                self.modified = True
            self.last_message_time[user_id] = datetime.datetime.now()
            if self.max_history > 0:
                self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
            self.save_to_file()  # Sauvegarde automatique après chaque ajout
            logging.info(f"[INFO] Mémoire mise à jour pour l'utilisateur {user_id}.")
            print(Fore.YELLOW + f"[INFO] Mémoire mise à jour pour l'utilisateur {user_id}." + Style.RESET_ALL)
            return self.conversations[user_id]
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la gestion de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la gestion de la mémoire" + Style.RESET_ALL)

    def get_history(self, user_id):
        """Récupère l'historique des messages d'un utilisateur."""
        try:
            logging.info("[INFO] Récupération de l'historique...")
            user_id = str(user_id)
            return self.conversations.get(user_id, [])
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la récupération de l'historique : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la récupération de l'historique" + Style.RESET_ALL)

    def save_to_file(self):
        try:
            logging.info("[INFO] Sauvegarde de la mémoire...")
            print(Fore.GREEN + "[INFO] Sauvegarde de la mémoire..." + Style.RESET_ALL)
            with open(settings.ROM_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "conversations": self.conversations,
                    "last_message_time": {k: v.isoformat() for k, v in self.last_message_time.items()}
                }, f, indent=4, ensure_ascii=False)
            self.modified = False
            logging.info("[INFO] Mémoire sauvegardée avec succès.")
            print(Fore.YELLOW + "[INFO] Mémoire sauvegardée avec succès." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la sauvegarde de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la sauvegarde de la mémoire" + Style.RESET_ALL)

    def load_from_file(self):
        """Charge la mémoire depuis un fichier JSON."""
        try:
            logging.info("[INFO] Vérification du fichier de mémoire...")
            if not os.path.exists(settings.ROM_PATH):
                return
            logging.info("[INFO] Fichier de mémoire verifié.")
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la vérification du fichier de mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la vérification du fichier de mémoire" + Style.RESET_ALL)
            return
        try:
            logging.info("[INFO] Chargement de la mémoire...")
            with open(settings.ROM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations = data.get("conversations", {})
                self.last_message_time = {
                    k: datetime.datetime.fromisoformat(v) for k, v in data.get("last_message_time", {}).items()
                }
            logging.info("[INFO] Mémoire chargée avec succès.")
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors du chargement de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors du chargement de la mémoire" + Style.RESET_ALL)

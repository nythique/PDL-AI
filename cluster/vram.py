import datetime, os, json, logging
from config import settings
from colorama import Fore, Style

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class memory:
    """Classe pour gérer le contexte utilisateur en mémoire vive avec persistance."""

    def __init__(self, max_history=settings.HISTORY_LIMIT):
        """Initialisation de la mémoire."""
        self.conversations = {}
        self.max_history = max_history
        self.last_message_time = {}
        self.load_from_file()

    def manage(self, user_id, message_content):
        """Ajoute un message au contexte utilisateur et limite l'historique."""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append(message_content)
        self.last_message_time[user_id] = datetime.datetime.now()

        # Limite l'historique à max_history messages
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
        return self.conversations[user_id]

    def clear_context(self, inactive_time_threshold=settings.MEMORY_CLEAR_TIME):
        """Nettoie les contextes des utilisateurs inactifs."""
        current_time = datetime.datetime.now()
        inactive_users = [
            user_id for user_id, last_message_time in self.last_message_time.items()
            if (current_time - last_message_time).total_seconds() > inactive_time_threshold
        ]
        for user_id in inactive_users:
            del self.conversations[user_id]
            del self.last_message_time[user_id]

    def get_history(self, user_id):
        """Récupère l'historique d'un utilisateur."""
        return self.conversations.get(user_id, [])

    def reset_user_context(self, user_id):
        """Réinitialise le contexte d'un utilisateur."""
        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self.last_message_time:
            del self.last_message_time[user_id]

    def save_to_file(self):
        """Sauvegarde l'état de la mémoire dans un fichier JSON."""
        try:
            with open(settings.MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "conversations": self.conversations,
                    "last_message_time": {k: v.isoformat() for k, v in self.last_message_time.items()}
                }, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(Fore.RED + f"[ERROR] Impossible de sauvegarder la mémoire : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Impossible de sauvegarder la mémoire : {e}")

    def load_from_file(self):
        """Charge l'état de la mémoire depuis un fichier JSON."""
        if not os.path.exists(settings.MEMORY_FILE):
            return
        try:
            with open(settings.MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations = data.get("conversations", {})
                self.last_message_time = {
                    k: datetime.datetime.fromisoformat(v) for k, v in data.get("last_message_time", {}).items()
                }
        except Exception as e:
            print(Fore.YELLOW + f"[ERROR] Impossible de charger la mémoire : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Impossible de charger la mémoire : {e}")
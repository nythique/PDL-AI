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
    def __init__(self, max_history=settings.HISTORY_LIMIT):
        self.conversations = {}
        self.max_history = max_history
        self.last_message_time = {}
        self.modified = False
        self.load_from_file()

    def clear_context(self, inactive_time_threshold=settings.MEMORY_CLEAR_MAX_TIME):
        """Supprime la mémoire des utilisateurs inactifs depuis plus de inactive_time_threshold secondes."""
        now = datetime.datetime.now()
        to_remove = []
        for user_id, last_time in self.last_message_time.items():
            if (now - last_time).total_seconds() > inactive_time_threshold:
                to_remove.append(user_id)
        for user_id in to_remove:
            self.conversations.pop(user_id, None)
            self.last_message_time.pop(user_id, None)
            self.modified = True

    def manage(self, user_id, message_content):
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
        return self.conversations[user_id]

    def get_history(self, user_id):
        user_id = str(user_id)
        return self.conversations.get(user_id, [])

    def save_to_file(self):
        try:
            with open(settings.MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "conversations": self.conversations,
                    "last_message_time": {k: v.isoformat() for k, v in self.last_message_time.items()}
                }, f, indent=4, ensure_ascii=False)
            self.modified = False
        except Exception as e:
            logging.error(f"[ERROR] Impossible de sauvegarder la mémoire : {e}")

    def load_from_file(self):
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
            logging.error(f"[ERROR] Impossible de charger la mémoire : {e}")
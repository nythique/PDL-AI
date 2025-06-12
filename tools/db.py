import json, os, sys, time, asyncio, logging, colorama,shutil
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Erreur lors du chargement de la base de données: {e}")
                return self.get_default_data()
        else:
            return self.get_default_data()

    def get_default_data(self):
        return {
            "Root Users": [],
            "Bot Status": "offline",
            "Allowed Channels": [],
            "Bot Stats": {
                "messages_sent": 0,
                "commands_executed": 0,
                "uptime": 0
            },
            "user_rankings": {}
        }

    def save_data(self):
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la base de données: {e}")

    def add_root_user(self, user_id):
        if user_id not in self.data["root_users"]:
            self.data["Root Users"].append(user_id)
            self.save_data()

    def remove_root_user(self, user_id):
        if user_id in self.data["root_users"]:
            self.data["Root Users"].remove(user_id)
            self.save_data()

    def set_bot_status(self, status):
        self.data["Bot status"] = status
        self.save_data()

    def add_allowed_channel(self, channel_id):
        if channel_id not in self.data["Allowed Channels"]:
            self.data["Allowed Channels"].append(channel_id)
            self.save_data()

    def remove_allowed_channel(self, channel_id):
        if channel_id in self.data["Allowed Channels"]:
            self.data["Allowed Channels"].remove(channel_id)
            self.save_data()

    def update_bot_stats(self, stat_name, value):
        if stat_name in self.data["Bot Stats"]:
            self.data["Bot Stats"][stat_name] = value
            self.save_data()

    def update_user_ranking(self, user_id, points):
        self.data["user_rankings"][user_id] = points
        self.save_data()

    def get_user_ranking(self, user_id):
        return self.data["user_rankings"].get(user_id, 0)

    def get_top_users(self, limit=10):
        sorted_users = sorted(self.data["user_rankings"].items(), key=lambda x: x[1], reverse=True)
        return sorted_users[:limit]

        """
        Exemple d'utilisation de la classe DatabaseManager :
        
        # Initialisation
        db = DatabaseManager("path/to/database.json")
        
        # Gestion des utilisateurs root
        db.add_root_user(123456789)
        db.remove_root_user(123456789)
        
        # Gestion du statut du bot
        db.set_bot_status("En ligne")
        
        # Gestion des canaux autorisés
        db.add_allowed_channel(987654321)
        db.remove_allowed_channel(987654321)
        
        # Mise à jour des statistiques
        db.update_bot_stats("messages_processed", 1500)
        db.update_bot_stats("commands_executed", 250)
        
        # Gestion des classements utilisateurs
        db.update_user_ranking(123456789, 100)
        points = db.get_user_ranking(123456789)
        top_users = db.get_top_users(5)
        
        # Sauvegarde automatique
        db.save_data()
        """
        
    def get_all_root_users(self):
        """Retourne la liste de tous les utilisateurs root"""
        return self.data.get("Root Users", [])
        
    def get_allowed_channels(self):
        """Retourne la liste de tous les canaux autorisés"""
        return self.data.get("Allowed Channels", [])
        
    def get_bot_status(self):
        """Retourne le statut actuel du bot"""
        return self.data.get("Bot status", "En maintenance")
        
    def get_bot_stats(self):
        """Retourne toutes les statistiques du bot"""
        return self.data.get("Bot Stats", {})
        
    def reset_user_ranking(self, user_id):
        """Remet à zéro le classement d'un utilisateur"""
        if user_id in self.data["user_rankings"]:
            del self.data["user_rankings"][user_id]
            self.save_data()
        
    def clear_all_rankings(self):
        """Supprime tous les classements utilisateurs"""
        self.data["user_rankings"] = {}
        self.save_data()
    
    def backup_database(self, backup_path):
        """Crée une sauvegarde de la base de données"""
        try:
            shutil.copy2(self.db_file, backup_path)
            logging.info(f"Sauvegarde créée: {backup_path}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde: {e}")
        
    def validate_data_integrity(self):
        """Vérifie l'intégrité des données"""
        required_keys = ["Root Users", "Bot status", "Allowed Channels", "Bot Stats", "user_rankings"]
        for key in required_keys:
            if key not in self.data:
                self.data[key] = {} if key in ["Bot Stats", "user_rankings"] else [] if key in ["Root Users", "Allowed Channels"] else "Inconnu"
        self.save_data()


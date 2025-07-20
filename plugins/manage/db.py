import json
import os
import sys
import time
import asyncio
import logging
import logging.handlers
import colorama
import shutil
from threading import RLock
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, SERVER_DB

# Constantes pour les clés de la base de données
ROOT_USERS_KEY = "Root Users"
BOT_STATUS_KEY = "Bot Status"
ALLOWED_CHANNELS_KEY = "Allowed Channels"
BOT_STATS_KEY = "Bot Stats"
USER_RANKINGS_KEY = "user_rankings"

# Configuration du logging
logger = logging.getLogger('database')
logger.setLevel(logging.INFO)

# Handler pour les logs de sécurité
info_handler = logging.FileHandler(
    SECURITY_LOG_PATH,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Handler pour les logs d'erreur
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

class Database:
    def __init__(self, db_file = SERVER_DB):
        self.db_file = db_file
        self._lock = RLock()
        self.data = self.load_data()
        self.validate_data_integrity()  # Vérifie l'intégrité dès le chargement

    def load_data(self):
        """Charge les données depuis le fichier JSON avec gestion des erreurs"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Base de données chargée depuis {self.db_file}")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Erreur de décodage JSON: {e}")
                return self.get_default_data()
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la base de données: {e}")
                return self.get_default_data()
        else:
            logger.info(f"Fichier {self.db_file} non trouvé, création d'une nouvelle base")
            return self.get_default_data()

    def get_default_data(self):
        """Retourne la structure par défaut de la base de données"""
        return {
            ROOT_USERS_KEY: [],
            BOT_STATUS_KEY: [
                "Je suis le G.O.A.T"
            ],
            ALLOWED_CHANNELS_KEY: [],
            BOT_STATS_KEY: {
                "messages_sent": 0,
                "commands_executed": 0,
                "uptime": 0
            },
            USER_RANKINGS_KEY: {}
        }

    def save_data(self):
        """Sauvegarde les données de manière atomique avec gestion des verrous"""
        with self._lock:
            temp_file = f"{self.db_file}.tmp"
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
                os.replace(temp_file, self.db_file)
                logger.info("Base de données sauvegardée avec succès")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde: {e}")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                raise

    def add_root_user(self, user_id):
        """Ajoute un utilisateur root avec validation"""
        with self._lock:
            if not isinstance(user_id, (int, str)):
                raise ValueError("user_id doit être un entier ou une chaîne")
            user_id = str(user_id)
            if user_id not in self.data[ROOT_USERS_KEY]:
                self.data[ROOT_USERS_KEY].append(user_id)
                self.save_data()
                logger.info(f"Utilisateur root ajouté: {user_id}")

    def remove_root_user(self, user_id):
        """Supprime un utilisateur root avec validation"""
        with self._lock:
            user_id = str(user_id)
            if user_id in self.data[ROOT_USERS_KEY]:
                self.data[ROOT_USERS_KEY].remove(user_id)
                self.save_data()
                logger.info(f"Utilisateur root supprimé: {user_id}")

    def set_bot_status(self, status):
        """Définit le statut du bot avec validation"""
        with self._lock:
            if not isinstance(status, (str, list)):
                raise ValueError("Le statut doit être une chaîne ou une liste")
            self.data[BOT_STATUS_KEY] = status if isinstance(status, list) else [status]
            self.save_data()
            logger.info(f"Statut du bot mis à jour: {status}")

    def add_allowed_channel(self, channel_id):
        """Ajoute un canal autorisé avec validation"""
        with self._lock:
            channel_id = str(channel_id)
            if channel_id not in self.data[ALLOWED_CHANNELS_KEY]:
                self.data[ALLOWED_CHANNELS_KEY].append(channel_id)
                self.save_data()
                logger.info(f"Canal ajouté aux autorisés: {channel_id}")

    def remove_allowed_channel(self, channel_id):
        """Supprime un canal autorisé"""
        with self._lock:
            channel_id = str(channel_id)
            if channel_id in self.data[ALLOWED_CHANNELS_KEY]:
                self.data[ALLOWED_CHANNELS_KEY].remove(channel_id)
                self.save_data()
                logger.info(f"Canal retiré des autorisés: {channel_id}")

    def update_bot_stats(self, stat_name, value):
        """Met à jour les statistiques du bot avec validation"""
        with self._lock:
            if stat_name not in self.data[BOT_STATS_KEY]:
                raise ValueError(f"Statistique inconnue: {stat_name}")
            self.data[BOT_STATS_KEY][stat_name] = value
            self.save_data()
            logger.info(f"Statistique mise à jour - {stat_name}: {value}")

    def update_user_ranking(self, user_id, points):
        """Met à jour le classement d'un utilisateur"""
        with self._lock:
            user_id = str(user_id)
            if not isinstance(points, (int, float)):
                raise ValueError("Les points doivent être un nombre")
            self.data[USER_RANKINGS_KEY][user_id] = points
            self.save_data()
            logger.info(f"Classement mis à jour - Utilisateur {user_id}: {points} points")

    def get_user_ranking(self, user_id):
        """Obtient le classement d'un utilisateur"""
        with self._lock:
            user_id = str(user_id)
            return self.data[USER_RANKINGS_KEY].get(user_id, 0)

    def get_top_users(self, limit=10):
        """Obtient le top des utilisateurs"""
        with self._lock:
            if not isinstance(limit, int) or limit < 1:
                raise ValueError("La limite doit être un entier positif")
            sorted_users = sorted(
                self.data[USER_RANKINGS_KEY].items(),
                key=lambda x: x[1],
                reverse=True
            )
            return sorted_users[:limit]
        
    def get_all_root_users(self):
        """Retourne la liste de tous les utilisateurs root"""
        with self._lock:
            return self.data.get(ROOT_USERS_KEY, [])
        
    def get_allowed_channels(self):
        """Retourne la liste de tous les canaux autorisés"""
        with self._lock:
            return self.data.get(ALLOWED_CHANNELS_KEY, [])
        
    def get_bot_status(self):
        """Retourne la liste des statuts du bot pour le cycle"""
        with self._lock:
            status = self.data.get(BOT_STATUS_KEY, "En maintenance")
            if isinstance(status, str):
                return [status]
            elif isinstance(status, list):
                return status
            else:
                return ["En maintenance"]
        
    def get_bot_stats(self):
        """Retourne toutes les statistiques du bot"""
        with self._lock:
            return self.data.get(BOT_STATS_KEY, {})
        
    def reset_user_ranking(self, user_id):
        """Remet à zéro le classement d'un utilisateur"""
        with self._lock:
            user_id = str(user_id)
            if user_id in self.data[USER_RANKINGS_KEY]:
                del self.data[USER_RANKINGS_KEY][user_id]
                self.save_data()
                logger.info(f"Classement réinitialisé pour l'utilisateur: {user_id}")
        
    def clear_all_rankings(self):
        """Supprime tous les classements utilisateurs"""
        with self._lock:
            self.data[USER_RANKINGS_KEY] = {}
            self.save_data()
            logger.info("Tous les classements ont été supprimés")
    
    def backup_database(self, backup_path):
        """Crée une sauvegarde de la base de données"""
        with self._lock:
            try:
                shutil.copy2(self.db_file, backup_path)
                logger.info(f"Sauvegarde créée: {backup_path}")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde: {e}")
                raise
        
    def validate_data_integrity(self):
        """Vérifie l'intégrité des données et initialise les valeurs manquantes"""
        with self._lock:
            default_values = {
                ROOT_USERS_KEY: [],
                BOT_STATUS_KEY: ["En maintenance"],
                ALLOWED_CHANNELS_KEY: [],
                BOT_STATS_KEY: {
                    "messages_sent": 0,
                    "commands_executed": 0,
                    "uptime": 0
                },
                USER_RANKINGS_KEY: {}
            }
            
            for key, default_value in default_values.items():
                if key not in self.data:
                    self.data[key] = default_value
                    logger.warning(f"Clé manquante {key} initialisée avec la valeur par défaut")
            
            self.save_data()
            logger.info("Validation de l'intégrité des données terminée")

    def migrate_data(self, version):
        """Migre les données vers une nouvelle structure
        
        Args:
            version (str): Version cible de la structure ('1.0', '2.0', etc.)
        """
        with self._lock:
            current_version = self.data.get('version', '1.0')
            
            if current_version == version:
                logger.info(f"La base de données est déjà en version {version}")
                return

            # Sauvegarde avant migration
            backup_path = f"{self.db_file}.backup_{current_version}"
            self.backup_database(backup_path)
            
            try:
                if version == '2.0' and current_version == '1.0':
                    # Exemple de migration de 1.0 vers 2.0
                    if 'user_rankings' in self.data:
                        # Restructuration du classement utilisateur
                        new_rankings = {}
                        for user_id, points in self.data['user_rankings'].items():
                            new_rankings[user_id] = {
                                'points': points,
                                'last_update': time.time(),
                                'achievements': []
                            }
                        self.data[USER_RANKINGS_KEY] = new_rankings
                        
                    # Ajout de nouvelles statistiques
                    self.data[BOT_STATS_KEY].update({
                        'voice_time': 0,
                        'commands_per_day': {}
                    })
                    
                    self.data['version'] = '2.0'
                    logger.info("Migration vers la version 2.0 réussie")
                
                # Ajouter d'autres migrations ici (2.0 -> 3.0, etc.)
                
                self.save_data()
                
            except Exception as e:
                logger.error(f"Erreur lors de la migration: {e}")
                # Restauration de la sauvegarde en cas d'erreur
                shutil.copy2(backup_path, self.db_file)
                logger.info("Restauration de la sauvegarde après échec de migration")
                raise


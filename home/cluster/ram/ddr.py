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
import os
import sys
import json
import logging
import datetime
import logging.handlers
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, ROM_LIMIT,ROM_PATH, MEMORY_MAX_INACTIVE_TIME

#======================================================================================
# ======================= INITIALISATION DES PARAMETRES DE LOGS =======================

logger = logging.getLogger('ddr')
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
# =================== GESTIONNAIRE DE MEMOIRE DDR1 (PREMIERE VERSION) =================
class ddr1:
    def __init__(self, maxHistory=ROM_LIMIT):
        try:
            logger.info("[INFO DDR]-> Initialisation de la mémoire en cours...")
            self.conversations = {}
            self.maxHistory = maxHistory
            self.lastMessageTime = {}
            self.modified = False
            self.loadFromFile()
            logger.info(f"[SUCCÈS DDR]-> Initialisation de la mémoire réussie.")
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 59.")
            print(f"[ERROR DDR]-> {e}, ligne 60.")

    def clearContext(self, inactiveTimeThreshold=MEMORY_MAX_INACTIVE_TIME * 3600):
        try:
            logger.info("[INFO DDR]-> Suppression de la mémoire des utilisateurs inactifs en cours...")
            now = datetime.datetime.now()
            toRemove = []
            for userID, lastTime in self.lastMessageTime.items():
                if (now - lastTime).total_seconds() > inactiveTimeThreshold:
                    toRemove.append(userID)
            for userID in toRemove:
                self.conversations.pop(userID, None)
                self.lastMessageTime.pop(userID, None)
                self.modified = True
                logger.info(f"[SUCCÈS DDR]-> Mémoire de l'utilisateurs {userID} supprimée avec succès.")
        except Exception as e:
            logger.error(f"[ERROR]-> {e}, ligne 76.")
            print(f"[ERROR DDR]-> {e}, ligne 77.")

    def manage(self, userID, messageContent):
        try:
            logger.info(f"[INFO DDR]-> Gestion de la mémoire de {userID} en cours ...")
            userID = str(userID)
            if userID not in self.conversations:
                self.conversations[userID] = []
            if not self.conversations[userID] or self.conversations[userID][-1] != messageContent:
                self.conversations[userID].append(messageContent)
                self.modified = True
            self.lastMessageTime[userID] = datetime.datetime.now()
            if self.maxHistory > 0:
                self.conversations[userID] = self.conversations[userID][-self.maxHistory:]
            self.saveToFile()
            logger.info(f"[SUCCÈS DDR]-> Gestion de la mémoire de {userID} réussie.")
            return self.conversations[userID]
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 95.")
            print(f"[ERROR DDR]-> {e}, ligne 96.")

    def getHistory(self, userID):
        try:
            logger.info(f"[INFO DDR]-> Récupération de l'historique {userID} en cours...")
            userID = str(userID)
            result = self.conversations.get(userID, [])
            logger.info(f"[SUCCÈS DDR]-> Récupération de l'historique {userID} en réussie.")
            return result 
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 106.")
            print(f"[ERROR DDR]-> {e}, ligne 107.")

    def saveToFile(self):
        try:
            logger.info("[INFO DDR]-> Session de sauvegarde de la mémoire en cours...")
            with open(ROM_PATH, "w", encoding="utf-8") as data:
                json.dump({
                    "conversations": self.conversations,
                    "lastMessageTime": {k: v.isoformat() for k, v in self.lastMessageTime.items()}
                }, data, indent=4, ensure_ascii=False)
            self.modified = False
            logger.info(f"[SUCCÈS DDR]-> Session de sauvegarde de la mémoire réussie.")
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 120.")
            print(f"[ERROR DDR]-> {e}, ligne 121.")

    def loadFromFile(self):
        try:
            logger.info("[INFO DDR]-> Vérification de la memoire rom en cours...")
            if not os.path.exists(ROM_PATH):
                logger.warring(f"[WARRING DDR]-> La memoire rom n'existe pas !")
            logger.info("[SUCCÈS DDR]-> Succès de la vérification de la memoire rom.")
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 130.")
            print(f"[ERROR DDR]-> {e}, ligne 131.")
        try:
            logger.info(f"[INFO DDR]-> Chargement de la mémoire en cours...")
            with open(ROM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations = data.get("conversations", {})
                self.lastMessageTime = {
                    k: datetime.datetime.fromisoformat(v) for k, v in data.get("lastMessageTime", {}).items()
                }
            logger.info(f"[SUCCÈS DDR]-> Succès du chargement de la mémoire.")
        except Exception as e:
            logger.error(f"[ERROR DDR]-> {e}, ligne 142.")
            print(f"[ERROR DDR]-> {e}, ligne 143.")
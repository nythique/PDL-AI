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
import time
import logging
import threading
import logging.handlers
from datetime import date
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH, SYSTEM_DB

# Ensure log and database directories exist to avoid FileHandler/File IO errors on import
try:
    for _path in (ERROR_LOG_PATH, SECURITY_LOG_PATH, SYSTEM_DB):
        dir_path = os.path.dirname(_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
except Exception as _e:
    # If directory creation fails during import, print to stdout but allow import to continue
    print(f"[WARN database] Could not ensure log/DB directories: {_e}")
#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('database')
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

# =====================================================================================
# ======================= GESTIONNAIRE DE LA BASE DE DONNEES ==========================

class database:

    def __init__(self, data = SYSTEM_DB):
        self.data = data
        # lock to protect concurrent read/write to the DB file
        self._lock = threading.Lock()
        self.loading = self.loadData()

    def loadData(self):
        try:
            logger.info(f"[INFO DATABASE]-> Vérification de l'existance du repertoire des données.")
            if os.path.exists(self.data) and os.path.getsize(self.data) > 0:
                try:
                    logger.info(f"[INFO DATABASE]-> Début du chargement des données.")
                    # protect read with lock to avoid race with writes
                    with self._lock:
                        with open(self.data, 'r', encoding='utf-8') as data:
                            dataLoading = json.load(data)
                    logger.info(f"[SUCCÈS DATABASE]-> Succès du chargement des données.")
                    return dataLoading
                except Exception as e:
                    logger.error(f"[ERROR DATABASE]-> {e}, ligne 67.")
            else:
                logger.warning(f"[WARNING DATABASE]-> Réinitialisation de la base des données en cours..")
                try:
                    resetDatabase = self.dataStructure()
                    self.loading = resetDatabase
                    self.saveData()
                    logger.info(f"[SUCCÈS DATABASE]-> Réinitialisation de la base des données")
                    return resetDatabase
                except Exception as e:
                    logger.error(f"[ERROR DATABASE]-> {e}, ligne 77.")
        except Exception as e:
            logger.error(f"[ERROR DATABASE]-> {e}, ligne 79.")
    
    def dataStructure(self):
        try:
            logger.info(f"[INFO DATABASE]-> Appel à la struture de la base de données.")
            return {
                "adminList":[],
                "userBlackList":[],
                "serverBlackList":[],
                "channelList":[1370867677333291149],
                "botStatusList":[],
                "botStats":{
                    "userNumber": 0,
                    "serverNumber": 0,
                    "QueryNumber": 0

                }
            }
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 98.")
    
    def saveData(self):
        try:
            logger.info(f"[INFO DATABASE]-> Opération de sauvegarde en cours..")
            # protect write with lock; write atomically by writing to temp and replacing
            tmp_path = f"{self.data}.tmp"
            with self._lock:
                with open(tmp_path, 'w', encoding='utf-8') as data_file:
                    json.dump(self.loading, data_file, indent=4, ensure_ascii=False)
                try:
                    os.replace(tmp_path, self.data)
                except Exception:
                    # fallback to simple write if atomic replace not available
                    with open(self.data, 'w', encoding='utf-8') as data_file:
                        json.dump(self.loading, data_file, indent=4, ensure_ascii=False)
            logger.info(f"[SUCCÈS DATABASE]-> Opération de sauvegarde réussie.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 107.")

    #-----------Fonctions d'insertions dans la base de données----------------------#

    def addAdmin(self, userID):
        try:
            logger.info(f"[INFO DATABASE]-> Ajout d'un nouveau administrateur en cours..")
            if isinstance(userID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération d'ajout de l'instance du nouveau administrateur lancées.")
                    if userID not in self.loading["adminList"]:
                        self.loading["adminList"].append(userID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération d'ajout de l'instance du nouveau administrateur reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant du nouveau administrateur exite déjà dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 125.")
            else:
                raise ValueError("userID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 129.")
    
    def addUserBlackList(self, userID):
        try:
            logger.info(f"[INFO DATABASE]-> Ajout d'un utilisateur banni en cours..")
            if isinstance(userID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération d'ajout de l'instance d'un utilisateur banni lancées.")
                    if userID not in self.loading["userBlackList"]:
                        self.loading["userBlackList"].append(userID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération d'ajout de l'instance d'un utilisateur banni reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant de l'utilisateur banni exite déjà dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 145.")
            else:
                raise ValueError("userID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 149.")
        
    def addServerBlackList(self, serverID):
        try:
            logger.info(f"[INFO DATABASE]-> Ajout d'un serveur banni en cours..")
            if isinstance(serverID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération d'ajout de l'instance d'un serveur banni lancées.")
                    if serverID not in self.loading["serverBlackList"]:
                        self.loading["serverBlackList"].append(serverID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération d'ajout de l'instance d'un serveur banni reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant du serveur banni exite déjà dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 165.")
            else:
                raise ValueError("serverID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 169.")

    def addChannelList(self, channelID):
        try:
            logger.info(f"[INFO DATABASE]-> Ajout d'un salon valide en cours..")
            if isinstance(channelID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération d'ajout de l'instance d'un salon valide lancées.")
                    if channelID not in self.loading["channelList"]:
                        self.loading["channelList"].append(channelID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération d'ajout de l'instance d'un salon valide reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant du salon valide exite déjà dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 185.")
            else:
                raise ValueError("channelID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 189.")

    def addBotStatusList(self, statusSTR):
        try:
            logger.info(f"[INFO DATABASE]-> Ajout d'un statut au bot en cours..")
            if isinstance(statusSTR, (str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération d'ajout d'un statut au bot lancées.")
                    if statusSTR not in self.loading["botStatusList"]:
                        self.loading["botStatusList"].append(statusSTR)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération d'ajout d'un statut au bot reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> Le statut exite déjà dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 205.") 
            else:
                raise ValueError("statusSTR doit-être une chaîne de caractère.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 209.")
    
    def updateBotStats(self, statsName, value):
        try:
            logger.info(f"[INFO DATABASE]-> Mise à jour d'une statistique du bot..")
            if isinstance(statsName, (str)) and isinstance(value, (int)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de mise à jour des statistiques lancées.")
                    if statsName in self.loading["botStats"]:
                        self.loading["botStats"][statsName]=value
                        self.saveData()
                        logger.info(f"[INFO DATABASE]-> Opération de mise à jour des statistiques réussie.")
                    else:
                        raise ValueError(f"Type de statistique inexistante: {statsName}")
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 224.")         
            else:
                raise ValueError(f"{statsName} et {value} doivent-être des chaînes de caractère.")
        except Exception as a:
            logger.info(f"[ERROR DATABASE]-> {a}, ligne 228.")
    
    #-----------Fonctions de suppression dans la base de données----------------------#

    def removeAdmin(self, userID):
        try:
            logger.info(f"[INFO DATABASE]-> Suppression d'un nouveau administrateur en cours..")
            if isinstance(userID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de suppression de l'instance d'un administrateur lancées.")
                    if userID in self.loading["adminList"]:
                        self.loading["adminList"].remove(userID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération de suppression de l'instance de l'administrateur reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant de l'administrateur n'exite pas dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as e:
                    logger.error(f"[ERROR DATABASE]-> {e}, ligne 246.")
        except Exception as e:
            logger.error(f"[ERROR DATABASE]-> {e}, ligne 248.")

    def removeUserBlackList(self, userID):
        try:
            logger.info(f"[INFO DATABASE]-> Libération d'un utilisateur banni en cours..")
            if isinstance(userID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de libération de l'instance d'un utilisateur banni lancées.")
                    if userID in self.loading["userBlackList"]:
                        self.loading["userBlackList"].remove(userID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération de libération  de l'instance d'un utilisateur banni reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant de l'utilisateur banni n'exite pas dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 264.")
            else:
                raise ValueError("userID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 268.")
        
    def removeServerBlackList(self, serverID):
        try:
            logger.info(f"[INFO DATABASE]-> Libération d'un serveur banni en cours..")
            if isinstance(serverID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de libération d'un serveur banni lancées.")
                    if serverID in self.loading["serverBlackList"]:
                        self.loading["serverBlackList"].remove(serverID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération de libération d'un serveur banni reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant du serveur banni n'exite pas dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 284.")
            else:
                raise ValueError("serverID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 288.")

    def removeChannelList(self, channelID):
        try:
            logger.info(f"[INFO DATABASE]-> Retrait d'un salon valide en cours..")
            if isinstance(channelID, (int, str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de retrait de l'instance d'un salon valide lancées.")
                    if channelID in self.loading["channelList"]:
                        self.loading["channelList"].remove(channelID)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération de retrait de l'instance d'un salon valide reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> L'instant du salon valide n'exite pas dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 304.")
            else:
                raise ValueError("channelID doit-être une chaîne de caractère ou un entier.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 308")

    def removeBotStatusList(self, statusSTR):
        try:
            logger.info(f"[INFO DATABASE]-> Retrait d'un statut du bot en cours..")
            if isinstance(statusSTR, (str)):
                try:
                    logger.info(f"[INFO DATABSE]-> Opération de retrait d'un statut du bot lancées.")
                    if statusSTR in self.loading["botStatusList"]:
                        self.loading["botStatusList"].remove(statusSTR)
                        self.saveData()
                        logger.info(f"[SUCCÈS DATABASE]-> Opération de retrait d'un statut du bot reussie.")
                    else:
                        logger.info(f"[ECHÈC DATABASE]-> Le statut n'exite pas dans la base de données.")
                        return f"Echèc de l'opération."
                except Exception as a:
                    logger.error(f"[ERROR DATABASE]-> {a}, ligne 324.") 
            else:
                raise ValueError("statusSTR doit-être une chaîne de caractère.")
        except Exception as a:
            logger.error(f"[ERROR DATABASE]-> {a}, ligne 328.")

    #-----------Fonction de sélection dans la base de données----------------------#
    
    def selectData(self, property):
        try:
            logger.info(f"[INFO DATABASE]-> Opération de sélection de la donnés {property} en cours ..")
            db = ["adminList","userBlackList","serverBlackList","channelList","botStatusList","botStats"]
            if property in db:
                try:
                    self.loading=self.loadData()
                    data = self.loading.get(property, []) # Récupère la donnée demandée ou une liste vide si elle n'existe pas
                    logger.info(f"[SUCCÈS DATABASE]-> Opération de sélection de la donnée {property} réussie.")
                    return data # Retourne la donnée demandée sous forme de liste ou de dictionnaire
                except Exception as e:
                    logger.error(f"[ERROR DATABASE]-> {e}, ligne 342.")
            else:
                logger.info(f"[ECHÈC DATABASE]-> La donnée {property} n'existe pas dans la base des données.")
                return f"Echèc de l'opération."
        except Exception as e:
            logger.error(f"[ERROR DATABASE]-> {e}, ligne 347.")
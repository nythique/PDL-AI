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
import psutil
import GPUtil
import logging
import platform
from datetime import datetime
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('node_vm')
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
# ======================= GESTIONNAIRE DU MONITORING ==================================

def hardwareInfo():
    try:
        logger.info(f"[INFO NODE-VM]-> Récuperration des données sur l'hébergeur en cours ..")
        result = {
            "timesTamp": datetime.now().isoformat(),
            "cpuUsage": psutil.cpu_percent(interval=1),
            "ramUsage": psutil.virtual_memory().percent,
            "diskUsage": psutil.disk_usage('/').percent,
            "networkIo": {
                "bytesSent": psutil.net_io_counters().bytes_sent,
                "bytesRecv": psutil.net_io_counters().bytes_recv
            },
            "gpus": [
                {
                    "id": gpu.id,
                    "load": gpu.load * 100,
                    "memoryUsed": gpu.memoryUsed,
                    "memoryTotal": gpu.memoryTotal
                } for gpu in GPUtil.getGPUs()
            ],
            "platform": platform.platform(),
            "processor": platform.processor()
        }
        logger.info(f"[SUCCÈS NODE-VM]-> Récuperration des données sur l'hébergeur en terminée.")
        return result
    except Exception as e:
        logger.error(f"[ERROR NODE-VM]-> {e}, ligne 57.")
        return None

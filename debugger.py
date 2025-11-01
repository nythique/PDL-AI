# ==================================================================================
# ========================== GESTION MEMOIRE DU BOT DISCORD ========================
# ==================================================================================    
# Auteur: @NYTHIQUE
# GitHub: https://github.com/Nythique
# Porfolio: https://nythique.github.io
# Description: Ce fichier contient le code principal du bot Discord PDL-IA.
# Date de création: 01/05/2020
# Licence: GNU AFFERO GENERAL PUBLIC LICENSE
#==================================================================================#
#++++++++++++++++++++++++++ LES IMPORTATIONS ++++++++++++++++++++++++++++++++++++++#
#==================================================================================#
import time
import colorama
import threading
import os
from colorama import Style, Fore
from plugins.integrating.storing.database import database
from plugins.integrating.hosting.node_vm import hardwareInfo
#==================================================================================#
#++++++++++++++++++++++++++ LES INITIALISATION ++++++++++++++++++++++++++++++++++++#
#==================================================================================#
colorama.init()
# DB instance is created only when running this script directly to avoid side-effects on import
db = None
#==================================================================================#
#++++++++++++++++++++++++++ LES FONCTIONS ++++++++++++++++++++++++++++++++++++++#
#==================================================================================#
def testDatabase():
    try:
        print(Fore.YELLOW + f"[TEST DATABASE START]-> Début du test du module database.py." + Style.RESET_ALL)

        db.addAdmin(12323545654)
        time.sleep(1)# Pause
        db.addUserBlackList(293958347983)
        time.sleep(1)# Pause
        db.addChannelList(1389375843)
        time.sleep(1)# Pause
        db.addServerBlackList(25342534534)
        time.sleep(1)# Pause
        db.addBotStatusList("salut ! Moi c'est le boncoin")
        time.sleep(1)# Pause
        db.updateBotStats("QueryNumber", 9)
        time.sleep(1)# Pause
        db.updateBotStats("serverNumber", 10)
        time.sleep(1)# Pause
        db.updateBotStats("userNumber", 11)
        time.sleep(1)# Pause
        db.removeAdmin(12323545654)
        time.sleep(1)# Pause
        db.removeUserBlackList(293958347983)
        time.sleep(1)# Pause
        db.removeChannelList(1389375843)
        time.sleep(1)# Pause
        db.removeServerBlackList(25342534534)
        time.sleep(1)# Pause
        db.removeBotStatusList("salut ! Moi c'est le boncoin")
        time.sleep(5)# Pause
        db.selectData("adminList")
        time.sleep(1)# Pause
        db.selectData("userBlackList")
        time.sleep(1)# Pause
        db.selectData("serverBlackList")
        time.sleep(1)# Pause
        db.selectData("channelList")
        time.sleep(1)# Pause
        db.selectData("botStatusList")
        time.sleep(1)# Pause
        db.selectData("botStats") # Sur forme de tableau (clé, valeur)
        time.sleep(1)# Pause

        print(Fore.GREEN + f"[TEST DATABASE END]-> Fin du test du module database.py." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[TEST DATABASE ERROR]-> {e}, ligne 62." + Style.RESET_ALL)

def testNodeVm():
    try:
        print(Fore.YELLOW + f"[TEST NODE-VM START]-> Début du test du module node_vm.py." + Style.RESET_ALL)
        hardwareInfo()
        time.sleep(1)# Pause
        print(Fore.GREEN + f"[TEST NODE-VM START]-> Fin du test du module node_vm.py."+ Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[TEST NODE-VM ERROR]-> {e}, ligne 71." + Style.RESET_ALL)
#==================================================================================#
#++++++++++++++++++++++++++ LES TESTS UNITAIRES +++++++++++++++++++++++++++++++++++#
#==================================================================================#
if __name__ == '__main__':
    # Ensure test DB directory exists
    test_db_path = os.path.join('unit-tests', 'data', 'data.json')
    test_db_dir = os.path.dirname(test_db_path)
    if test_db_dir and not os.path.exists(test_db_dir):
        try:
            os.makedirs(test_db_dir, exist_ok=True)
        except Exception as e:
            print(Fore.RED + f"[TEST SETUP ERROR]-> Could not create test DB directory: {e}" + Style.RESET_ALL)
            raise

    # initialize DB for tests
    db = database(test_db_path)

    th1 = threading.Thread(target=testDatabase)
    th2 = threading.Thread(target=testNodeVm)

    th1.start()
    th2.start()

    th1.join()
    th2.join()


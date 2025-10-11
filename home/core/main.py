# home/core/main.py
# ==================================================================================
# ========================== FICHIER PRINCIPAL DU BOT DISCORD ======================
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
import time
import discord
import asyncio
import logging
from itertools import cycle
from datetime import datetime
from home.gen.ollama import ollama
from home.cluster.ram.ddr import ddr1
from discord.ext import commands, tasks
from plugins.integrating.storing.database import database
from plugins.processing.recognition.ocr import OCRProcessor as ocr 
from config.settings import UNAUTHO_WORDS, SYSTEM_DB, NAME_IA, TESSERACT_PATH
from config.settings import  STATUS_TIME, ROM_UPDATE_TIME, MEMORY_CLEAR_TIME, PROMPT_SYSTEM, TYPING_TIME

#========================================================================================================
# ==================================== INITIALISATION DES PARAMETRES DES MODULES ========================

bot = None
status = None
keyWord = NAME_IA

nlp = ollama()
userMemory = ddr1()
db = database(SYSTEM_DB)
ocr_analyser = ocr(tesseract_path=TESSERACT_PATH)


#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('main')
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

#========================================================================================================
# ==================================== FONCTIONS UTILES =================================================

@tasks.loop(seconds=STATUS_TIME)
async def statusSwap():
    try:
        logger.info(f"[INFO MAIN]-> Changement du statut du bot en cours...")
        global status
        statusList = db.selectData("botStatusList")
        if not hasattr(statusSwap, "cycle") or statusSwap.cycle_list != statusList:
            statusSwap.cycle = cycle(statusList)
            statusSwap.cycle_list = statusList
        currentStatus = next(statusSwap.cycle)
        await bot.change_presence(activity=discord.CustomActivity(currentStatus))
        logger.info(f"[SUCCÈS MAIN]-> Changement de statut réussi.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 82.")
        print(f"[ERROR MAIN]-> {e}, ligne 83.")

@statusSwap.before_loop
async def beforeStatusSwap(): 
    try:
        logger.info(f"[INFO MAIN]-> En attente que le bot soit prêt pour démarrer le changement de statut...")
        await bot.wait_until_ready()
        logger.info(f"[INFO MAIN]-> Attente terminée le changement de statut peut démarrer.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 92.")
        print(f"[ERROR MAIN]-> {e}, ligne 93.")

@tasks.loop(minutes=ROM_UPDATE_TIME)
async def saveMemoryPeriodically():
    try:
        logger.info(f"[INFO MAIN]-> Opération de sauvegarde périodique de la mémoire en cours...")
        if userMemory.modified:
            userMemory.saveToFile()
            userMemory.modified = False
            logger.info(f"[SUCCÈS MAIN]-> Opération de sauvegarde périodique de la mémoire réussie.")
        else:
            logging.info("[INFO MAIN]-> Opération de sauvegarde périodique de la mémoire annulée.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 106.")
        print(f"[ERROR MAIN]-> {e}, ligne 107.")

@saveMemoryPeriodically.before_loop
async def beforeSaveMemory():  
    try:
        logger.info(f"[INFO MAIN]-> En attente que le bot soit prêt pour démarrer la sauvegarde périodique de la mémoire...")
        await bot.wait_until_ready()
        logger.info(f"[INFO MAIN]-> Attente terminée la sauvegarde périodique de la mémoire peut démarrer.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 116.")
        print(f"[ERROR MAIN]-> {e}, ligne 117.")

@tasks.loop(minutes=MEMORY_CLEAR_TIME)
async def clearInactiveUsers():   
    try:
        logger.info(f"[INFO MAIN]-> Nettoyage intelligent des utilisateurs inactifs en cours...")
        for userID in userMemory.conversations.keys():  
            userMemory.clearContext()
        userMemory.saveToFile() 
        logger.info(f"[SUCCÈS MAIN]-> Nettoyage intelligent des utilisateurs inactifs réussi.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 128.")
        print(f"[ERROR MAIN]-> {e}, ligne 129.")

@clearInactiveUsers.before_loop
async def beforeClearInactiveUsers():  
    try:
        logger.info(f"[INFO MAIN]-> En attente que le bot soit prêt pour démarrer le nettoyage des utilisateurs inactifs...")
        await bot.wait_until_ready()
        logger.info(f"[INFO MAIN]-> Attente terminée le nettoyage des utilisateurs inactifs peut démarrer.")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 138.")
        print(f"[ERROR MAIN]-> {e}, ligne 139.")

"""                 NOTE: Système Lavalink (En développement)
@tasks.loop(seconds=10)
async def checkEmptyVoiceChannels():  
    try:
        for voice_client in bot.voice_clients: 
            if voice_client.channel:
                members = [m for m in voice_client.channel.members if not m.bot]
                if not members:
                    guild_id = voice_client.guild.id
                    player = await lavalink_manager.get_player(guild_id)
                    if player:
                        await player.stop()
                        await player.disconnect()
                    await voice_client.disconnect()
                    logging.info(f"[VOICE] Déconnecté du salon vocal vide dans le serveur {voice_client.guild.name} (ID: {voice_client.guild.id})")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de la vérification des salons vocaux" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de la vérification des salons vocaux : {e}")

@checkEmptyVoiceChannels.before_loop
async def before_checkEmptyVoiceChannels():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux...")
        await bot.wait_until_ready() # type: ignore
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux : {e}")
"""

def displayBanner():
    banner = """
        ██████╗ ██████╗  ██╗         █████╗ ██╗
        ██╔══██╗██╔══██╗ ██║        ██╔══██╗██║
        ██████╔╝██║  ██║ ██║        ███████║██║
        ██╔═══╝ ██║  ██║ ██║        ██╔══██║██║
        ██║     ██████╔╝ ███████╗██╗██║  ██║██║
        ╚═╝     ╚═════╝  ╚══════╝╚═╝╚═╚═╝╚═╝╚═╝
    """
    version = os.getenv("VERSION") 
    currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    licenseMessage = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   This software is developed by @NYTHIQUE on 01/05/2020.         ║
║   All rights reserved.                                           ║
║                                                                  ║
║   Version: {version}                                             ║
║   Bot started on: {currentDate}                                  ║
║                                                                  ║
║   Unauthorized copying, distribution, or modification of this    ║
║   software is strictly prohibited. Use is subject to the terms   ║
║   of the license agreement.                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)
    time.sleep(1)
    print(licenseMessage)

#========================================================================================================
# ============================= ENREGISTREMENT DES EVENEMENTS TEXTE ET VOCAUX ===========================
def registerCommands(botInstance):
    try:
        global bot, music_manager
        bot = botInstance
        displayBanner()
        logger.info("[INFO MAIN]-> Démarrage des évènements primcipaux...")
    except Exception as e:
        logger.error(f"[ERROR MAIN]-> {e}, ligne 210.")
        print(f"[ERROR MAIN]-> {e}, ligne 210.")

    @bot.event
    async def on_ready():
        try:
            logger.info("[INFO MAIN]-> Démarrage des tâches périodiques en cours...")
            if not saveMemoryPeriodically.is_running():
                saveMemoryPeriodically.start()
            if not clearInactiveUsers.is_running():
                clearInactiveUsers.start()
            try:
                global status
                status = cycle(db.selectData("botStatusList"))
                if not statusSwap.is_running():
                    statusSwap.start()
            except Exception as e:
                logger.error(f"[ERROR MAIN]-> {e}, ligne 227.")
                print(f"[ERROR MAIN]-> {e}, ligne 228.")
            logger.info(f"[SUCCÈS MAIN]-> Démarrage des tâches périodiques en terniné.")
        except Exception as e:
            logger.error(f"[ERROR MAIN]-> {e}, ligne 231.")
            print(f"[ERROR MAIN]-> {e}, ligne 232.")

        try:   
            logger.info("[INFO MAIN]-> Processus de synchronisation des commandes en cours...")
            client = bot.user 
            synced = await bot.tree.sync()
            logger.info("[INFO MAIN]-> Processus de synchronisation des commandes en terminé.")
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
            print(f"[SUCCÈS MAIN]-> {len(synced)} commandes synchronisées avec succès !")
            print(f"[INFO MAIN]-> {len(bot.guilds)} serveurs connectés !")
            print(f"[INFO MAIN]-> Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
            print(f"[SUCCÈS MAIN]-> {client.name} est prêt et en ligne !\n")
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
            logger.info(f"[INFO MAIN]-> Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
            logger.info(f"[SUCCÈS MAIN]-> {client.name} est prêt et en ligne !")
        except Exception as e:
            logger.error(f"[ERROR MAIN]-> {e}, ligne 248.")
    
    # =========================================================================================================
    # ==================================== LOGIQUE DES MESSAGES INTERACTIFS ===================================
    @bot.event
    async def on_message(message):
        if message.author.bot: return 
        if message.channel.id not in db.selectData("channelList"): return
        if any(key in message.content for key in UNAUTHO_WORDS):
            await message.channel.send(f"Je ne peux pas te répondre. Tu as utilisé une mauvaise expression.")
            return
        
        content = message.content.strip()
        userID = message.author.id
 
        mentionTrue = bot.user.mention in message.content
        keyWordTrue = any(keyword in message.content for keyword in keyWord)
        referenceTrue = message.reference and message.reference.resolved and message.reference.resolved.author == bot.user 
        
        # ------------------------------ Gestion des commandes interactives vocales (En Dev)-------------------------------- #
        """
        for cmd, keywords in music_commands.items():
            if any(keyword in content.lower() for keyword in keywords):
                music_command = cmd
                break
        try:
                if any(cmd in message.content.lower() for cmd in music_commands["play"]):
                    query = message.content.split("lance la musique")[-1].strip()
                    await music_player.play_music(message, query)
                    return

                elif any(cmd in message.content.lower() for cmd in music_commands["stop"]):
                    await music_player.stop_music(message)
                    return

                elif any(cmd in message.content.lower() for cmd in music_commands["pause"]):
                    await music_player.pause_music(message)
                    return

                elif any(cmd in message.content.lower() for cmd in music_commands["resume"]):
                    await music_player.resume_music(message)
                    return
                
                elif any(cmd in message.content.lower() for cmd in music_commands["volume"]):
                    try:
                        volume = int(message.content.split("à")[-1].strip())
                        await music_player.set_volume(message, volume)
                    except ValueError:
                        await message.channel.send("Volume invalide (0-100)")
                    return
        except Exception as e:
                logging.error(f"[ERROR] Erreur lors du traitement de la commande musicale : {e}")
                await message.channel.send("Une erreur s'est produite lors du traitement de la commande musicale.")
                return
        """

        # ----------------------------------- Gestion des commandes interactices spéciales ----------------------------------- #
        if any(key in content.lower() for key in ordre_restart) and (mentionTrue or keyWordTrue or referenceTrue):
            if message.author.id in db.selectData("adminList"):
                try:
                    await message.reply(f"Je me redémarre, merci de patienter {message.author.name} 🤧.")
                    logger.warring(f"[INFO MAIN]-> L'administrateur {message.author.name} à demandé le redémarrage du pdlai.")
                    await bot.close() 
                except Exception as e:
                    logger.error(f"[ERROR MAIN]-> {e}, ligne 312.")
                    return
            else:
                await message.reply(f"C'est bien essayé. Mais tu n'as pas les bonnes permissions pour me faire dormir !")
                logger.warring(f"[INFO MAIN]-> L'utilisateur {message.author.name} à essayé de faire redémarrer pdlai.")

        if any(key in content.lower() for key in numberMember) and (mentionTrue or keyWordTrue or referenceTrue):
            try:
                guild = message.guild
                memberCount = guild.member_count 
                await message.reply(f"Il y a actuellement {memberCount} membres sur le serveur.")
                return
            except Exception as e:
                await message.reply(f"Je ne peux pas te dire combien de membres il y a sur le serveur pour l'instant.")
                logger.error(f"[INFO MAIN]-> {e}, ligne 326.")
                return           
        # ----------------------------------- Gestion des messages texte ---------------------------------------------- #
        if isinstance(message.channel, discord.DMChannel) or bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user: # type: ignore
            try:
                # ------------------------------------- Gestion des pièces jointes --------------------------------- #
                if message.attachments:
                    for attachment in message.attachments:
                        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                            async with message.channel.typing():
                                extracted_text = await ocr_analyser.process_attachment(attachment)
                                if extracted_text.strip():
                                    content += f" {extracted_text}"
                                    logger.info(f"[INFO MAIN]-> Texte extrait ajouté au message.")
                                else:
                                    logger.info("[INFO MAIN]-> Aucun texte détecté dans l'image.")
                            break
                        # ------------------------------  Gestion des fichiers audio  ----------------------------------
                        """
                        if any(attachment.filename.lower().endswith(ext) for ext in ['wav', 'mp3', 'ogg', 'm4a']):
                            async with message.channel.typing():
                                audio_file = await attachment.read()
                                texte = await speech_to_text(audio_file)
                                if texte.strip():
                                    userContext = userMemory.manage(userID, texte)
                                    username = message.author.name
                                    systemPrompt = (
                                        settings.PROMPT +
                                        f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " +
                                        "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. Sois naturel et pertinent."
                                    )
                                    messages = []
                                    messages.append({"role": "system", "content": systemPrompt})
                                    for msg in userContext:
                                        if isinstance(msg, dict) and "role" in msg and "content" in msg:
                                            messages.append({"role": msg["role"], "content": msg["content"]})
                                        else:
                                            messages.append({"role": "user", "content": str(msg)})
                                    messages.append({"role": "user", "content": texte})
                                    response = nlp.get_answer(messages, username=username)
                                    audio_path = await text_to_speech(response, userID)
                                    if message.author.voice and message.author.voice.channel:
                                        voice_channel = message.author.voice.channel
                                        voice_client = discord.utils.get(bot.voice_clients, guild=voice_channel.guild)
                                        if not voice_client or not voice_client.is_connected():
                                            voice_client = await voice_channel.connect()
                                        if voice_client.is_playing():
                                            voice_client.stop()
                                        audio_source = discord.FFmpegPCMAudio(audio_path)
                                        voice_client.play(audio_source)
                                        await message.reply("Réponse vocale envoyée !")
                                    else:
                                        await message.reply(response)
                                else:
                                    await message.reply("Je n'ai pas compris le message vocal.")
                            return
                        """
                # ---------------------------------- Gestion de la conversation ------------------------------------ #
                userContext = userMemory.manage(userID, content)
                username = message.author.name
                userID = message.author.id  
 
                systemPrompt = (
                    PROMPT_SYSTEM +
                    f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas. " +
                    "Sois naturel et pertinent.\n"
                )

                messages = []
                messages.append({"role": "system", "content": systemPrompt})
                for msg in userContext:
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    else:
                        messages.append({"role": "user", "content": str(msg)})
                messages.append({"role": "user", "content": content})
                async with message.channel.typing():
                    await asyncio.sleep(TYPING_TIME)
                    response = nlp.getAnswer(messages, username=username)
                    await message.reply(response)
                return
            except Exception as e:
                await message.reply("Une erreur cririque s'est produite. Veulliez réessayer plus tard et le signaler si vous le voulez bien (/help).")
                logging.error(f"[ERROR MAIN]-> {e}, ligne 410.")  

        await bot.process_commands(message) 
    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

# =========================================================================================================
# ==================================== GESTION DES ÉVÉNEMENTS LAVALINK ====================================
""" 
@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(Fore.GREEN + f"[LAVALINK] Node {node.identifier} prêt!" + Style.RESET_ALL)
    logging.info(f"[LAVALINK] Node {node.identifier} prêt!")

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    try:
        await music_player.handle_track_end(player)
    except Exception as e:
        logging.error(f"[MUSIC] Erreur de fin de piste: {e}")

@bot.event
async def on_wavelink_node_unavailable(node: wavelink.Node):
    print(Fore.RED + f"[LAVALINK] Node {node.identifier} déconnecté!" + Style.RESET_ALL)
    logging.warning(f"[LAVALINK] Node {node.identifier} déconnecté!")
"""
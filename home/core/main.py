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
# ========================= IMPORTATIONS ==========================================
import os
import time
import discord
import logging
import asyncio
import wavelink 
import colorama 

from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from colorama import Fore, Style

from config import settings
from config.settings import UNAUTHO_WORDS, SYSTEM_DB

from home.gen.smart import ollama
from home.cluster.ram.ddr import ddr1
from home.gen.music import MusicPlayer

from plugins.processing.recognition.orc import OCRProcessor as ocr 
from plugins.integrating.storing.database import Database
from plugins.integrating.hosting.node_lavalink import LavalinkManager

from commands.custom.interact import ordre_restart, numberMember, voc_ordre, voc_exit, music_commands

#========================================================================================================
# ==================================== INITIALISATION DES PARAMETRES DES MODULES ========================
colorama.init()
#-------------------------------
db = Database(SYSTEM_DB)
#------------------------------
nlp = ollama()
keyWord = settings.NAME_IA
user_memory = ddr1()
#------------------------------
ocr_analyser = ocr(tesseract_path=settings.TESSERACT_PATH)
#------------------------------
lavalink_manager = LavalinkManager()
music_player = MusicPlayer(lavalink_manager)
#------------------------------
bot = None
status = None

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

#========================================================================================================
# ==================================== FONCTIONS UTILES =================================================
def slowType(text, delay=settings.SLOWTYPE_TIME):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

@tasks.loop(seconds=settings.STATUS_TIME)
async def status_swap():
    try:
        global status
        db.load_data()
        status_list = db.get_bot_status()
        if not hasattr(status_swap, "cycle") or status_swap.cycle_list != status_list:
            status_swap.cycle = cycle(status_list)
            status_swap.cycle_list = status_list
        current_status = next(status_swap.cycle)
        await bot.change_presence(activity=discord.CustomActivity(current_status))
        logging.info(f"[INFO] Statut changé : {current_status}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du changement de statut" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors du changement de statut : {e}")

@status_swap.before_loop
async def before_status_swap():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer le changement de statut..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer le changement de statut...")
        await bot.wait_until_ready() # type: ignore
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant le changement de statut" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant le changement de statut : {e}")

@tasks.loop(minutes=settings.ROM_UPDATE_TIME)
async def save_memory_periodically():
    try:
        print(Fore.CYAN + "[INFO] Sauvegarde périodique de la mémoire..." + Style.RESET_ALL)
        logging.info(f"[INFO] Sauvegarde périodique de la mémoire...")
        if user_memory.modified:
            user_memory.save_to_file()
            user_memory.modified = False
            print(Fore.GREEN + "[INFO] Sauvegarde de la mémoire réussie." + Style.RESET_ALL)
            logging.info(f"[INFO] Sauvegarde de la mémoire réussie.")
        else:
            logging.info("[INFO] Aucune modification détectée dans la mémoire. Sauvegarde ignorée.")
            print(Fore.YELLOW + "[INFO] Aucune modification détectée dans la mémoire. Sauvegarde ignorée." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ERROR] La sauvegarde périodique de la mémoire a échoué" + Style.RESET_ALL)
        logging.error(f"[ERROR] La sauvegarde périodique de la mémoire a échoué : {e}")

@save_memory_periodically.before_loop
async def before_save_memory():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer la sauvegarde périodique..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer la sauvegarde périodique...")
        await bot.wait_until_ready() # type: ignore
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant la sauvegarde périodique" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant la sauvegarde périodique : {e}")

@tasks.loop(minutes=settings.MEMORY_CLEAR_TIME)
async def clear_inactive_users():
    try:
        print(Fore.CYAN + "[INFO] Nettoyage intelligent des utilisateurs inactifs..." + Style.RESET_ALL)
        logging.info(f"[INFO] Nettoyage intelligent des utilisateurs inactifs...")
        
        # Utilisez le nettoyage intelligent au lieu du nettoyage simple
        for user_id in user_memory.conversations.keys():
            # Évaluation de la performance d'apprentissage
            user_memory._evaluate_learning_performance()
            # Nettoyage intelligent de l'historique
            user_memory._smart_trim_history(user_id)
        
        user_memory.save_to_file()
        print(Fore.GREEN + "[INFO] Nettoyage intelligent des utilisateurs inactifs réussi." + Style.RESET_ALL)
        logging.info(f"[INFO] Nettoyage intelligent des utilisateurs inactifs réussi.")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Le nettoyage des utilisateurs inactifs a échoué : {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Le nettoyage des utilisateurs inactifs a échoué : {e}")

@clear_inactive_users.before_loop
async def before_clear_inactive_users():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer le nettoyage des inactifs..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer le nettoyage des utilisateurs inactifs...")
        await bot.wait_until_ready() # type: ignore
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant le nettoyage des utilisateurs inactifs" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant le nettoyage des utilisateurs inactifs : {e}")

@tasks.loop(seconds=10)
async def check_empty_voice_channels():
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

@check_empty_voice_channels.before_loop
async def before_check_empty_voice_channels():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux...")
        await bot.wait_until_ready() # type: ignore
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux : {e}")

def display_banner():
    banner = """
██████╗ ██████╗  ██╗         █████╗ ██╗
██╔══██╗██╔══██╗ ██║        ██╔══██╗██║
██████╔╝██║  ██║ ██║        ███████║██║
██╔═══╝ ██║  ██║ ██║        ██╔══██║██║
██║     ██████╔╝ ███████╗██╗██║  ██║██║
╚═╝     ╚═════╝  ╚══════╝╚═╝╚═╚═╝╚═╝╚═╝
"""
    version = os.getenv("VERSION")
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    license_message = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   This software is developed by @NYTHIQUE on 01/05/2020.         ║
║   All rights reserved.                                           ║
║                                                                  ║
║   Version: {version}                                             ║
║   Bot started on: {current_date}                                 ║
║                                                                  ║
║   Unauthorized copying, distribution, or modification of this    ║
║   software is strictly prohibited. Use is subject to the terms   ║
║   of the license agreement.                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    slowType(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + license_message + Style.RESET_ALL)

#========================================================================================================
# ============================= ENREGISTREMENT DES EVENEMENTS TEXTE ET VOCAUX ===========================
def register_commands(bot_instance):
    global bot, music_manager
    bot = bot_instance
    display_banner()
    logging.info("[INFO] Connexion aux API discord...")
    try:
        lavalink_manager.connect_nodes(bot)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Erreur de connexion aux nœuds Lavalink : {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Erreur de connexion aux nœuds Lavalink : {e}")

    @bot.event
    async def on_ready():
        try:
            print(Fore.YELLOW + "[INFO] Démarrage des tâches périodiques..." + Style.RESET_ALL)
            logging.info("[INFO] Démarrage des tâches périodiques...")
            if not save_memory_periodically.is_running():
                save_memory_periodically.start()
            if not clear_inactive_users.is_running():
                clear_inactive_users.start()
            if not check_empty_voice_channels.is_running():
                check_empty_voice_channels.start()

            try:
                global status
                status = cycle(db.get_bot_status())
                if not status_swap.is_running():
                    status_swap.start()
            except Exception as e:
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage de la tâche de changement de statut {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage de la tâche de changement de statut : {e}")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques : {e}")

        try:   
            logging.info("[INFO] Démarrage de la tache de synchronisation...")
            print(Fore.YELLOW + "[INFO] Démarrage de la tache de synchronisation..." + Style.RESET_ALL)
            client = bot.user # type: ignore
            synced = await bot.tree.sync() # type: ignore 
            print(Fore.GREEN + f"[INFO] {len(synced)} commandes synchronisées avec succès !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(synced)} commandes synchronisées avec succès !")
            print(Fore.GREEN + f"[INFO] {len(bot.guilds)} serveurs connectés !" + Style.RESET_ALL) # type: ignore
            logging.info(f"[INFO] {len(bot.guilds)} serveurs connectés !") # type: ignore
            print(Fore.GREEN + f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !" + Style.RESET_ALL)
            logging.info(f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
            slowType(Fore.LIGHTGREEN_EX + f"[START] Le bot est prêt et en ligne !\n" + Style.RESET_ALL)
            logging.info(f"[START] Le bot est prêt et en ligne !")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes : {e}")
    
    # =========================================================================================================
    # ==================================== LOGIQUE DES MESSAGES INTERACTIFS ===================================
    @bot.event
    async def on_message(message):
        db.load_data()
        if message.author.bot: return 
        if message.channel.id not in db.get_allowed_channels(): return
        if any(key in message.content for key in UNAUTHO_WORDS):
            await message.channel.send(f"Je ne peux pas te répondre. Parlons d'autres choses.")
            return
        
        content = message.content.strip()
        user_id = message.author.id

        voc_orde_true = any(key in content for key in voc_ordre)
        voc_exit_true = any(key in content for key in voc_exit)
        music_command = None
        mention_true = bot.user.mention in message.content # type: ignore
        keyWord_true = any(keyword in message.content for keyword in keyWord)
        reference_true = message.reference and message.reference.resolved and message.reference.resolved.author == bot.user # type: ignore
        
        # ------------------------------ Gestion des commandes interactives vocales --------------------------------
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
    

        # ----------------------------------- Gestion des commandes interactices spéciales -----------------------------------
        if any(key in content.lower() for key in ordre_restart) and (mention_true or keyWord_true or reference_true):
            if message.author.id in settings.ROOT_USER:
                try:
                    await message.reply(f"Je me redémarre, merci de ta patience {message.author.name} 🤧")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    await bot.close() # type: ignore
                except Exception as e:
                    await message.reply(f"C'est bien essayé, mais je ne peux pas redémarrer avec tes permissions !")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    return

        if any(key in content.lower() for key in numberMember) and (mention_true or keyWord_true or reference_true):
            try:
                guild = message.guild
                member_count = guild.member_count
                await message.reply(f"Il y a actuellement {member_count} membres sur le serveur.")
                print(Fore.YELLOW + f"[INFO] Demande de nombre de membres sur le serveur : {message.author.name}" + Style.RESET_ALL)
                logging.info(f"[INFO] Demande de nombre de membres sur le serveur : {message.author.name}")
                return
            except Exception as e:
                await message.reply(f"Je ne peux pas te dire combien de membres il y a sur le serveur !")
                print(Fore.YELLOW + f"[INFO] Demande de nombre de membres sur le serveur : {message.author.name}" + Style.RESET_ALL)
                logging.info(f"[INFO] Demande de nombre de membres sur le serveur : {message.author.name}")
                return           
        # ----------------------------------- Gestion des messages texte -----------------------------------
        if isinstance(message.channel, discord.DMChannel) or bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user: # type: ignore
            try:

                # ------------------------------------- Gestion des pièces jointes ---------------------------------
                if message.attachments:
                    for attachment in message.attachments:
                        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                            async with message.channel.typing():
                                extracted_text = await ocr_analyser.process_attachment(attachment)
                                if extracted_text.strip():
                                    content += f" {extracted_text}"
                                    print(Fore.CYAN + f"[INFO] Texte extrait ajouté au message" + Style.RESET_ALL)
                                    logging.info(f"[INFO] Texte extrait ajouté au message : {extracted_text}")
                                else:
                                    print(Fore.YELLOW + "[INFO] Aucun texte détecté dans l'image." + Style.RESET_ALL)
                                    logging.info("[INFO] Aucun texte détecté dans l'image.")
                            break
                        # ------------------------------  Gestion des fichiers audio  ----------------------------------
                        """
                        if any(attachment.filename.lower().endswith(ext) for ext in ['wav', 'mp3', 'ogg', 'm4a']):
                            async with message.channel.typing():
                                audio_file = await attachment.read()
                                texte = await speech_to_text(audio_file)
                                if texte.strip():
                                    user_context = user_memory.manage(user_id, texte)
                                    username = message.author.name
                                    system_prompt = (
                                        settings.PROMPT +
                                        f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " +
                                        "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. Sois naturel et pertinent."
                                    )
                                    messages = []
                                    messages.append({"role": "system", "content": system_prompt})
                                    for msg in user_context:
                                        if isinstance(msg, dict) and "role" in msg and "content" in msg:
                                            messages.append({"role": msg["role"], "content": msg["content"]})
                                        else:
                                            messages.append({"role": "user", "content": str(msg)})
                                    messages.append({"role": "user", "content": texte})
                                    response = nlp.get_answer(messages, username=username)
                                    audio_path = await text_to_speech(response, user_id)
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
                # ------------------------------  Fin gestion des pièces jointes  ----------------------------------
                # ---------------------------------- Gestion de la conversation -----------------------------------
                user_context = user_memory.manage(user_id, content)
                username = message.author.name
                user_id = message.author.id

                system_prompt = (
                    settings.PROMPT_SYSTEM +
                    f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. " +
                    "Sois naturel et pertinent.\n"
                )

                messages = []
                messages.append({"role": "system", "content": system_prompt})
                for msg in user_context: # type: ignore
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    else:
                        messages.append({"role": "user", "content": str(msg)})
                messages.append({"role": "user", "content": content})

                print(Fore.YELLOW + f"[INFO] Une interaction est en cours dans le serveur" + Style.RESET_ALL)
                logging.info(f"[INFO] Une interaction est en cours dans le serveur")
                async with message.channel.typing():
                    await asyncio.sleep(settings.TYPING_TIME)
                    response = nlp.get_answer(messages, username=username)
                    await message.reply(response)
                return
            except Exception as e:
                await message.reply("Désolé, une erreur s'est produite lors du traitement de votre demande")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors d'une interaction dans le serveur : {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Une erreur s'est produite lors d'une interaction dans le serveur : {e}")  

        await bot.process_commands(message) # type: ignore
    
    @bot.event
    async def on_command_error(ctx, error):
        """Gestion des erreurs de commande préfix"""
        if isinstance(error, commands.CommandNotFound):
            return

# =========================================================================================================
# ==================================== GESTION DES ÉVÉNEMENTS LAVALINK ======================================  
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
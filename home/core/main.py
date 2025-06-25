from home.gen.smart import ollama
from colorama import Fore, Style
from config import settings
from config.settings import BAD_WORDS
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from home.cluster.vram import memory
from home.gen.music import LavalinkManager
from plugins.ocr import OCRProcessor as ocr
from plugins.voc import Speechio as voc
from plugins.utils.db import Database
from commands.custom.interact import ordre_restart, numberMember, voc_ordre, voc_exit, music_commands
import discord, time, logging, asyncio, colorama
colorama.init()

db = Database(settings.SERVER_DB)
db.backup_database(settings.SERVER_BACKUP)
nlp = ollama()
keyWord = settings.NAME_IA
user_memory = memory()
ocr_analyser = ocr(tesseract_path=settings.TESSERACT_PATH)
music_manager = None
bot = None

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


def slowType(text, delay=settings.SLOWTYPE_TIME):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

status = cycle(db.get_bot_status()) 

@tasks.loop(seconds=settings.STATUS_TIME)
async def status_swap():
    try:
        global status
        status = cycle(db.get_bot_status())
        current_status = next(status)
        await bot.change_presence(activity=discord.CustomActivity(current_status))
        logging.info(f"[INFO] Statut changé : {current_status}")
        try:
            db.load_data()
        except Exception as a:
            print(Fore.RED + f"[LOAD DATA] Erreuir lors du chargement des données.")
            logging.error(f"[LOAD DATA] Erreur de donée chargé: {a}.")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du changement de statut" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors du changement de statut : {e}")

@status_swap.before_loop
async def before_status_swap():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer le changement de statut..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer le changement de statut...")
        await bot.wait_until_ready()
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
        await bot.wait_until_ready()
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant la sauvegarde périodique" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant la sauvegarde périodique : {e}")

@tasks.loop(minutes=settings.MEMORY_CLEAR_TIME)
async def clear_inactive_users():
    try:
        print(Fore.CYAN + "[INFO] Nettoyage des utilisateurs inactifs..." + Style.RESET_ALL)
        logging.info(f"[INFO] Nettoyage des utilisateurs inactifs...")
        user_memory.clear_context()
        user_memory.save_to_file()  
        print(Fore.GREEN + "[INFO] Nettoyage des utilisateurs inactifs réussi." + Style.RESET_ALL)
        logging.info(f"[INFO] Nettoyage des utilisateurs inactifs réussi.")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Le nettoyage des utilisateurs inactifs a échoué : {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Le nettoyage des utilisateurs inactifs a échoué : {e}")

@clear_inactive_users.before_loop
async def before_clear_inactive_users():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer le nettoyage des inactifs..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer le nettoyage des utilisateurs inactifs...")
        await bot.wait_until_ready()
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant le nettoyage des utilisateurs inactifs" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant le nettoyage des utilisateurs inactifs : {e}")

@tasks.loop(seconds=10)
async def check_empty_voice_channels():
    """Vérifie si le bot est seul en vocal et le fait quitter"""
    try:
        for voice_client in bot.voice_clients:
            if voice_client.channel:
                members_in_channel = [member for member in voice_client.channel.members if not member.bot]
                
                if len(members_in_channel) == 0:
                    await voice_client.disconnect()
                    print(Fore.YELLOW + f"[INFO] Bot déconnecté du salon vocal vide : {voice_client.channel.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Bot déconnecté du salon vocal vide : {voice_client.channel.name}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Erreur lors de la vérification des salons vocaux vides : {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Erreur lors de la vérification des salons vocaux vides : {e}")

@check_empty_voice_channels.before_loop
async def before_check_empty_voice_channels():
    try:
        print(Fore.YELLOW + "[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente que le bot soit prêt pour démarrer la vérification des salons vocaux...")
        await bot.wait_until_ready()
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors de l'attente avant la vérification des salons vocaux : {e}")

#=============()
def display_banner():
    banner = """
    ██████╗ ██████╗  ██╗         █████╗ ██╗
    ██╔══██╗██╔══██╗ ██║        ██╔══██╗██║
    ██████╔╝██║  ██║ ██║        ███████║██║
    ██╔═══╝ ██║  ██║ ██║        ██╔══██║██║
    ██║     ██████╔╝ ███████╗██╗██║  ██║██║
    ╚═╝     ╚═════╝  ╚══════╝╚═╝╚═╚═╝╚═╝╚═╝
    """
    version = settings.VERSION
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    license_message = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   This software is developed by @NYTHIQUE on 01/05/2020.         ║
    ║   All rights reserved.                                           ║
    ║                                                                  ║
    ║   Version: {version}                               ║
    ║   Bot started on: {current_date}                            ║
    ║                                                                  ║
    ║   Unauthorized copying, distribution, or modification of this    ║
    ║   software is strictly prohibited. Use is subject to the terms   ║
    ║   of the license agreement.                                      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    slowType(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + license_message + Style.RESET_ALL)

def register_commands(bot_instance):
    global bot, music_manager
    bot = bot_instance
    music_manager = LavalinkManager(bot)
    display_banner()
    logging.info("[INFO] Connexion aux API discord...")
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
                if not status_swap.is_running():
                    status_swap.start()
            except Exception as e:
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage de la tâche de changement de statut {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage de la tâche de changement de statut : {e}")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques : {e}")
        
        try:
            # Initialisation de Lavalink
            print(Fore.YELLOW + "[INFO] Initialisation de Lavalink..." + Style.RESET_ALL)
            logging.info("[INFO] Initialisation de Lavalink...")
            await music_manager.setup_lavalink()
            
            logging.info("[INFO] Démarrage de la tache de synchronisation...")
            print(Fore.YELLOW + "[INFO] Démarrage de la tache de synchronisation..." + Style.RESET_ALL)
            client = bot.user
            synced = await bot.tree.sync()
            print(Fore.GREEN + f"[INFO] {len(synced)} commandes synchronisées avec succès !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(synced)} commandes synchronisées avec succès !")
            print(Fore.GREEN + f"[INFO] {len(bot.guilds)} serveurs connectés !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(bot.guilds)} serveurs connectés !")
            print(Fore.GREEN + f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !" + Style.RESET_ALL)
            logging.info(f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
            slowType(Fore.LIGHTGREEN_EX + f"[START] Le bot est prêt et en ligne !\n" + Style.RESET_ALL)
            logging.info(f"[START] Le bot est prêt et en ligne !")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes : {e}")

    @bot.event
    async def on_lavalink_node_ready(payload):
        await music_manager.on_lavalink_node_ready(payload)

    @bot.event
    async def on_lavalink_track_end(payload):
        await music_manager.on_lavalink_track_end(payload)

    @bot.event
    async def on_message(message):
        if message.author.bot: return 
        if message.channel.id not in db.get_allowed_channels(): return
        if any(key in message.content for key in BAD_WORDS):
            await message.channel.send(f"Je ne peux pas te répondre. Parlons d'autres choses.")
            return
        
        content = message.content.strip()
        user_id = message.author.id

        voc_orde_true = any(key in content for key in voc_ordre)
        voc_exit_true = any(key in content for key in voc_exit)
        music_command = None
        mention_true = bot.user.mention in message.content
        keyWord_true = any(keyword in message.content for keyword in keyWord)
        reference_true = message.reference and message.reference.resolved and message.reference.resolved.author == bot.user
        
        for cmd, keywords in music_commands.items():
            if any(keyword in content.lower() for keyword in keywords):
                music_command = cmd
                break

        if music_command and (mention_true or keyWord_true or reference_true):
            try:
                if music_command == "help_music":
                    embed = music_manager.create_music_embed(
                        "Option musicale",
                        """
                        **🎵 Intéractions Musicales Disponibles :**
                        
                        **Lecture :**
                        • `pdl joue [recherche/URL]` - Lance une musique depuis YouTube
                        • `pdl lance [recherche/URL]` - Lance une musique depuis YouTube
                        
                        **Contrôle :**
                        • `pdl stop` - Arrête la musique
                        • `pdl pause` - Met en pause
                        • `pdl reprend` - Reprend la lecture
                        • `pdl volume [0-100]` - Change le volume
                        
                        **Exemples :**
                        • `pdl joue despacito`
                        • `pdl lance https://youtube.com/watch?v=...`
                        • `pdl volume 50`
                        
                        **Sources supportées :** YouTube, SoundCloud, Bandcamp, Vimeo
                        """,
                        discord.Color.green()
                    )
                    await message.reply(embed=embed)
                    return

                elif music_command == "stop":
                    if bot.voice_clients:
                        for voice_client in bot.voice_clients:
                            if await music_manager.stop_playback(voice_client.channel.guild.id):
                                await message.reply("J'ai arrêté la musique !.")
                                return
                        await message.reply(f"Il n'y a rien à arrêter {message.author.name}.")
                    else:
                        await message.reply(f"T'es pas en vocal avec moi {message.author.name}.")
                    return

                elif music_command == "pause":
                    if bot.voice_clients:
                        for voice_client in bot.voice_clients:
                            if await music_manager.pause_playback(voice_client.channel.guild.id):
                                await message.reply("Je te laisse reprendre ton soufle.")
                                return
                        await message.reply("Tu aimes bien la desinformation.")
                    else:
                        await message.reply(f"T'es pas en vocal avec moi {message.author.name}.")
                    return

                elif music_command == "resume":
                    if bot.voice_clients:
                        for voice_client in bot.voice_clients:
                            if await music_manager.resume_playback(voice_client.channel.guild.id):
                                await message.reply("La partie reprend 😏")
                                return
                        await message.reply("Il y avait quoi en pause déjà ? RIEN !")
                    else:
                        await message.reply(f"T'es pas en vocal avec moi {message.author.name}.")
                    return

                elif music_command == "volume":
                    words = content.split()
                    volume = None
                    
                    for i, word in enumerate(words):
                        if any(keyword in word.lower() for keyword in music_commands["volume"]):
                            if i + 1 < len(words):
                                try:
                                    volume = int(words[i + 1])
                                    break
                                except ValueError:
                                    pass
                    
                    if volume is None or volume < 0 or volume > 100:
                        await message.reply(f"Un volume de {volume}, 💀 Je pourrai pas t'aider.")
                        return

                    if bot.voice_clients:
                        for voice_client in bot.voice_clients:
                            if await music_manager.set_volume(voice_client.channel.guild.id, volume):
                                await message.reply(f"J'ai adjusté le volume à {volume}% 😎.")
                                return
                        await message.reply("Bon bah, t'as pas de chance, j'ai pas réeussi à changer le volume 😜.")
                    else:
                        await message.reply(f"T'es pas en vocal avec moi {message.author.name}.")
                    return

                elif music_command == "play":
                    words = content.split()
                    music_query = None
                    
                    for i, word in enumerate(words):
                        if any(keyword in word.lower() for keyword in music_commands["play"]):
                            if i + 1 < len(words):
                                music_query = " ".join(words[i + 1:])
                                break
                    
                    if not music_query:
                        await message.reply("Je dois jouer quoi ? soit compréhensible !")
                        return

                    if not message.author.voice or not message.author.voice.channel:
                        await message.reply("Rejoins un salon vocal pour écouter de la musique avec moi 😤.")
                        return
                    try:
                        print(Fore.CYAN + f"[MUSIC] Recherche de la musique: {music_query}" + Style.RESET_ALL)
                        logging.info(f"[MUSIC] Recherche de la musique: {music_query}")
                        
                        track = await music_manager.search_track(music_query)
                        
                        if not track:
                            await message.reply(f"J'ai pas trouvé le son. Vérifiez si tu ne t'est pas planté 🤥.")
                            logging.warning(f"[MUSIC] Aucune musique trouvée pour: {music_query}")
                            return

                        if await music_manager.join_voice_channel(message.author.voice.channel):
                            if await music_manager.play_track(message.author.voice.channel.guild.id, track):
                                # Récupération des informations de la piste avec lavalink.py
                                title = getattr(track, 'title', 'Unknown')
                                author = getattr(track, 'author', 'Unknown')
                                duration = music_manager.format_duration(getattr(track, 'length', 0))
                                
                                embed = music_manager.create_music_embed(
                                    "🎵 Lecture en cours",
                                    f"**Titre :** {title}\n**Artiste :** {author}\n**Durée :** {duration}\n**Salon :** {message.author.voice.channel.name}",
                                    discord.Color.green()
                                )
                                await message.reply(embed=embed)
                                print(Fore.GREEN + f"[MUSIC] Musique lancée avec succès: {title}" + Style.RESET_ALL)
                                logging.info(f"[MUSIC] Musique lancée avec succès: {title}")
                            else:
                                await message.reply("Je crois mon serveur musical à pété. Reviens plus tard tenter ta chance 🤧.")
                                logging.error(f"[MUSIC] Erreur lors de la lecture de la musique pour: {music_query}")
                        else:
                            await message.reply("J'ai pas les permissions pour te rejoindre en vocal. tu peux que t'en vouloir 😤.")
                            logging.error(f"[MUSIC] Impossible de rejoindre le salon vocal: {message.author.voice.channel.name}")
                            
                    except Exception as e:
                        await message.reply(f"Petite ou grosse erreur lorsque je recherchais la musicque. Fais un ``/set report`` pour le signaler 🥲.")
                        print(Fore.RED + f"[MUSIC] Erreur lors de la recherche: {e}" + Style.RESET_ALL)
                        logging.error(f"[MUSIC] Erreur lors de la recherche de '{music_query}': {e}")
                    return

            except Exception as e:
                await message.reply("J'ai pas correctement compris ta demande . On réseille ?")
                logging.error(f"[MUSIC] Erreur lors de la commande musicale : {e}")
                return

        if voc_exit_true and (mention_true or keyWord_true or reference_true):
            try:
                if bot.voice_clients:
                    for voice_client in bot.voice_clients:
                        await voice_client.disconnect()
                    await message.reply(f"J'ai quitté le salon vocal 🤧.")
                    logging.info(f"[INFO] Le bot a quitté le salon vocal sur demande de {message.author.name}")
                    return
                else:
                    await message.reply(f"Je ne suis pas connecté en vocal !")
                    return
            except Exception as e:
                await message.reply(f"Je ne peux pas quitter le salon vocal ! Envoie un `/set report` pour me signaler l'erreur.")
                logging.error(f"[ERROR] Une erreur s'est produite lors de la déconnexion vocale : {e}")
                return

        if voc_orde_true and (mention_true or keyWord_true or reference_true):
            try:
                if message.author.voice and message.author.voice.channel:
                    voc_channel = message.author.voice.channel
                    if not any(Vc.channel == voc_channel for Vc in bot.voice_clients):
                        await voc_channel.connect()
                        await message.reply(f"Je tes rejoint dans le salon vocal !")
                        logging.info(f"[INFO] Le bot a rejoint le salon vocal : {voc_channel.name}")
                        return
                    else:
                        await message.reply(f"Je suis déjà dans un salon vocal !")
                        return
                else:
                    await message.reply(f"Rejoins un salon vocal pour que je puisse te rejoindre !")
                    logging.warning(f"[WARNING] L'utilisateur {message.author.name} n'est pas dans un salon vocal !")
                    return
            except Exception as e:
                await message.reply(f"Je ne peux pas te rejoindre dans un salon vocal ! Envoie un `/set report` pour me signaler l'erreur.")
                logging.error(f"[ERROR] Une erreur s'est produite lors de la reconnaissance de l'ordre de voc : {e}")
                return

        if any(key in content for key in ordre_restart) and (mention_true or keyWord_true or reference_true):
            if message.author.id in settings.ROOT_USER:
                try:
                    await message.reply(f"Je me redémarre, merci de ta patience {message.author.name} 🤧")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    await bot.close()
                except Exception as e:
                    await message.reply(f"C'est bien essayé, mais je ne peux pas redémarrer avec tes permissions !")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    return

        if any(key in content for key in numberMember) and (mention_true or keyWord_true or reference_true):
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

        if isinstance(message.channel, discord.DMChannel) or bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user:
            try:
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

                user_context = user_memory.manage(user_id, content)
                username = message.author.name
                user_id = message.author.id

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

        await bot.process_commands(message)
        
    @bot.event
    async def on_voice_state_update(member, before, after):
        try:
            if before.channel and not after.channel:
                for voice_client in bot.voice_clients:
                    if voice_client.channel == before.channel:
                        remaining_members = [m for m in before.channel.members if not m.bot]
                        
                        if len(remaining_members) == 0:
                            await voice_client.disconnect()
                            print(Fore.YELLOW + f"[INFO] Bot déconnecté automatiquement du salon vocal vide : {before.channel.name}" + Style.RESET_ALL)
                            logging.info(f"[INFO] Bot déconnecté automatiquement du salon vocal vide : {before.channel.name}")
                        break
        except Exception as e:
            print(Fore.RED + f"[ERROR] Erreur lors de la gestion de l'événement voice_state_update : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Erreur lors de la gestion de l'événement voice_state_update : {e}")
        
    @bot.event
    async def on_command_error(ctx, error):
        """Gestion des erreurs de commande préfix"""
        if isinstance(error, commands.CommandNotFound):
            return

 
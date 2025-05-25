from home.gen.smart import ollama
from colorama import Fore, Style
from config import settings
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput, Select
from home.cluster.vram import memory
from tools.ocr import OCRProcessor as ocr
import discord, time, os, sys, json, logging, asyncio
import colorama
colorama.init()

nlp = ollama()
status = settings.STATUS
keyWord = settings.NAME_IA
user_memory = memory()
ocr_analyser = ocr(tesseract_path=settings.TESSERACT_PATH)
bot = None


"""Handler pour les logs info et warning"""
info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""Handler pour les logs error"""
error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""On réinitialise la config root et on ajoute les handlers"""
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)


def slowType(text, delay=settings.SLOWTYPE_TIME):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

status = cycle(status) 
@tasks.loop(seconds=settings.STATUS_TIME)
async def status_swap(bot):
    """Change le statut du bot Discord à intervalle régulier"""
    try:
        await bot.change_presence(activity=discord.CustomActivity(next(status)))
        logging.info(f"[INFO] Statut changé : {next(status)}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du changement de statut" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors du changement de statut : {e}")

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
        user_memory.save_to_file()  # <-- sauvegarder le nettoyage dans la ROM
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
    global bot
    bot = bot_instance
    """Afficher la bannière de démarrage"""
    display_banner()
    """Connexion aux api discord"""
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
            if not status_swap.is_running():
                status_swap.start(bot)
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques : {e}")
        
        try:
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
    async def on_message(message):
        if message.author.bot: return 
        if message.channel.id in settings.BLOCKED_CHANNEL_ID: return

        content = message.content.strip()
        user_id = message.author.id
        ordre_restart = ["Redémarre toi","redémarre toi","va faire dodo"]
        numberMember = ["Combien de membres sur le serveur","combien de membres sur le serveur", "Nombres de membres sur le serveur","nombres de membres sur le serveur", "Nombre de membre","nombre de membre", "number of members on the server"]
        

        if any(key in content for key in ordre_restart):
            if message.author.id in settings.ROOT_UER:
                try:
                    await message.reply(f"Je vais redémarrer, merci de votre patience !")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    await bot.close()
                except Exception as e:
                    await message.reply(f"C'est bien essayé, mais je ne peux pas redémarrer avec ton ordre !")
                    print(Fore.YELLOW + f"[INFO] Demande de redémarrage du bot par : {message.author.name}" + Style.RESET_ALL)
                    logging.info(f"[INFO] Demande de redémarrage du bot par : {message.author.name}")
                    return

        if any(key in content for key in numberMember):
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
#((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))    

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

                # Construction du prompt système sans l'ID
                system_prompt = (
                    settings.PROMPT +
                    f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. Sois naturel et pertinent."
                )

                # Construction de la liste messages pour l'IA
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
        
#(((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))

    @bot.event
    async def on_command_error(ctx, error):
        """Gestion des erreurs de commande préfix"""
        if isinstance(error, commands.CommandNotFound):
            return

    @bot.command(name="errors")
    async def errors(ctx, lines: int = 10):
        """Affiche les dernières lignes du fichier de logs d'erreur."""
        await ctx.message.delete() #"""Supprime le message de la commande"""
        await ctx.defer() #"""Défère la réponse pour éviter le timeout"""
        """Vérifie si l'utilisateur a les permissions nécessaires"""
    
        if ctx.author.id not in settings.ROOT_UER:
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {ctx.author.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {ctx.author.name}")
            return
        log_path = settings.ERROR_LOG_PATH
        if not os.path.exists(log_path):
            await ctx.send("Le fichier de logs d'erreur n'existe pas.")
            return
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines_content = f.readlines()[-lines:]
            if not lines_content:
                await ctx.send("Aucune erreur trouvée dans les logs.")
                return
            msg = "```" + "".join(lines_content)[-1900:] + "```"
            await ctx.send(msg)
            print(Fore.GREEN + f"[INFO] Logs d'erreur envoyés" + Style.RESET_ALL)
            logging.info(f"[INFO] Logs d'erreur envoyés à {ctx.author.name}")
        except Exception as e:
            await ctx.send(f"Erreur lors de la lecture des logs.")
            print(Fore.RED + f"[ERROR] Erreur lors de la lecture des logs" + Style.RESET_ALL)
            logging.error(f"[ERROR] Erreur lors de la lecture des logs : {e}")

    @bot.command(name="ping")
    async def ping(ctx):
        """Affiche la latence du bot et de Discord dans un embed."""
        try:
            await ctx.message.delete() #"""Supprime le message de la commande"""
            await ctx.defer() #"""Défère la réponse pour éviter le timeout"""
        except Exception:
            pass  # Ignore si le bot n'a pas la permission
    
        bot_latency = round(bot.latency * 1000)

        if bot_latency < 150:
            embed = discord.Embed(
                title=f"🏓 Bonne latence : {bot_latency} ms",
                color=discord.Color.green()
            )
            embed.set_footer(text="PDL AI • .gg/pcpdl")
            await ctx.send(embed=embed)
        elif bot_latency > 150:
            embed = discord.Embed(
                title=f"🏓 Mauvaise latence : {bot_latency} ms",
                color=discord.Color.orange()
            )
            embed.set_footer(text="PDL AI • .gg/pcpdl")
            await ctx.send(embed=embed)
        print(Fore.GREEN + f"[INFO] Ping demandé par {ctx.author.name}" + Style.RESET_ALL)
        logging.info(f"[INFO] Ping demandé par {ctx.author.name}")

#(((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))

    @bot.tree.command(name="restart", description="Redémarrer le bot.")
    async def restart(interaction: discord.Interaction):
        if not interaction.user.id in settings.ROOT_UER:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}")
            return
        try:
            client = bot.user
            await interaction.response.send_message(f"🔄 {client.name} va redémarrer...", ephemeral=True)
            print(Fore.MAGENTA + f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}")
            await bot.close()
        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur s'est produite lors du redémarrage : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}"+ Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}")
            return
    

    @bot.tree.command(name="empty", description="Vider les fichiers de logs.")
    async def empty(interaction: discord.Interaction):
        if interaction.user.id not in settings.ROOT_UER:
            await interaction.response.send_message("Attention ! Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}")
            return
        files_to_clear = {
            "Log File (Sécurité)": settings.SECURITY_LOG_PATH,
            "Log File (Erreur)": settings.ERROR_LOG_PATH,
        }
        errors = []
        for file_name, file_path in files_to_clear.items():
            try:
                print(Fore.YELLOW + f"[INFO] Vidage de {file_name}. Demandé par {interaction.user.name}" + Style.RESET_ALL)
                logging.info(f"[INFO] Vidage de {file_name}. Demandé par {interaction.user.name}")
                if not os.path.exists(file_path):
                    errors.append(f"{file_name} n'existe pas.")
                    continue
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("")
                print(Fore.GREEN + f"[INFO] {file_name} a été vidé." + Style.RESET_ALL)
                logging.info(f"[INFO] {file_name} a été vidé. Demandé par {interaction.user.name}")
            except Exception as e:
                errors.append(f"Erreur lors du vidage de {file_name} : {e}")
                logging.error(f"[ERROR] Erreur lors du vidage de {file_name} : {e}")
                print(Fore.RED + f"[ERROR] Erreur lors du vidage de {file_name}" + Style.RESET_ALL)
        if errors:
            error_message = "\n".join(errors)
            await interaction.response.send_message(f"Des erreurs se sont produites :\n{error_message}", ephemeral=True)
            logging.error(f"[ERROR] Des erreurs se sont produites :{error_message}")
            print(Fore.RED + f"[ERROR] Des erreurs se sont produites" + Style.RESET_ALL)
        else:
            try:
                await interaction.response.send_message("Tous les fichiers de logs ont été vidés avec succès.", ephemeral=True)
                print(Fore.GREEN + f"[INFO] Tous les fichiers de logs ont été vidés avec succès." + Style.RESET_ALL)
            except Exception as e:
                logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'imformation à {interaction.user.name} : {e}")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'imformation à {interaction.user.name}" + Style.RESET_ALL)

    @bot.tree.command(name="help", description="Afficher l'aide du bot.")
    async def help(interaction: discord.Interaction):
        try:
            bot_user = bot.user
            embed = discord.Embed(
                title="Aide de PDL IA",
                description="Voici les principales commandes et fonctionnalités du bot :",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=bot_user.display_avatar.url)
            embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
            embed.add_field(name="/empty", value="Vider les fichiers logs", inline=False)
            embed.add_field(name="/restart", value="Redémarre le bot (admin seulement).", inline=False)
            embed.add_field(name="Préfix p.", value="errors <num>, voir les errors du logging", inline=False)
            embed.add_field(name="Préfix p.", value="ping , voir la latence du bot", inline=False)
            embed.add_field(name="Interaction", value="Mentionne le bot ou utilise son nom pour discuter avec lui.", inline=False)
            embed.add_field(name="OCR", value="Envoie une image contenant du texte en DM ou sur le serveur pour que le bot l'analyse.", inline=False)
            embed.set_footer(text="Développé par Nythique • PDL IA")
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot"
            embed.add_field(name="Lien d'invitation", value=f"[Clique ici pour inviter le bot]({invite_url})", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(Fore.GREEN + f"[INFO] Message d'aide envoyé à {interaction.user.name}" + Style.RESET_ALL)
            logging.info(f"[INFO] Message d'aide envoyé à {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de l'envoi de l'aide : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}")

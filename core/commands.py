from ia.nlp import HybridNLPEngine
from colorama import Fore, Style
from config import settings
from itertools import cycle
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput, Select
from cluster.vram import memory
import discord, time, os, sys, json, logging, asyncio

nlp = HybridNLPEngine()
status = settings.STATUS

TEMP_QR = {}
SUGGESTION_FILE = settings.CAPTURE_QR_PATH

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def save_suggestion(q, r):
    try:
        print(Fore.CYAN + f"[INFO] Sauvegarde de q/r lancée" + Style.RESET_ALL)
        logging.info(f"[INFO] Sauvegarde de q/r lancée")
        with open(SUGGESTION_FILE, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append({"question": q, "reponse": r})
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(Fore.RED + f"[ERROR] La sauvegarde q/r (ligne 31) à échoué: {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] La sauvegarde q/r (ligne 31) à échoué: {e}")

def slowType(text, delay=0.2):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

status = cycle(status) 
@tasks.loop(seconds=5)
async def status_swap(bot):
    await bot.change_presence(activity=discord.CustomActivity(next(status)))
    print(Fore.YELLOW + f"[INFO] Changement de statut en cours..." + Style.RESET_ALL)
    logging.info(f"[INFO] Changement de statut en cours...")

def register_commands(bot):
    from core.validation import register_validation
    register_validation(bot)
    slowType(Fore.RED + "   Développé par NYTHIQUE le 01/05/2020.\n" + Style.RESET_ALL, 0.1)
    time.sleep(1)
    print(Fore.CYAN + "[INFO] Connexion à l'API discord" + Style.RESET_ALL)
    logging.info(f"[INFO] Connexion à l'API discord")
    @bot.event
    async def on_ready():
        status_swap.start(bot)
        try:
            client = bot.user
            synced = await bot.tree.sync()
            print(Fore.GREEN + f"[INFO] {len(synced)} commandes synchronisées avec succès !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(synced)} commandes synchronisées avec succès !")
            print(Fore.GREEN + f"[INFO] {len(bot.guilds)} serveurs connectés !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(bot.guilds)} serveurs connectés !")
            print(Fore.GREEN + f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !" + Style.RESET_ALL)
            logging.info(f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de la connexion : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de la connexion : {e}")
        print(Fore.YELLOW + "[INFO] En attente des messages..." + Style.RESET_ALL)
        logging.info(f"[INFO] En attente des messages...")

    @bot.event
    async def on_message(message):

        channel_id = message.channel.id
        content = message.content.strip()
        
        if message.author.bot: return # Ignore les messages des bots

        if isinstance(message.channel, discord.DMChannel):
            try:
                print(Fore.YELLOW + f"[INFO] Une interaction en DM est en cours" + Style.RESET_ALL)
                logging.info(f"[INFO] Une interaction en DM est en cours")
                async with message.channel.typing():
                    await asyncio.sleep(2)
                    response = nlp.get_answer(message.content)
                    await message.channel.send(response)
                return
            except Exception as e:
                await message.channel.send("Désolé, une erreur s'est produite lors du traitement de votre message.")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors d'une interaction en DM : {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Une erreur s'est produite lors de la réponse en DM : {e}")
        keyWord = settings.NAME_IA
        if bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user:
            try:
                print(Fore.YELLOW + f"[INFO] Une interaction est en cours dans le serveur" + Style.RESET_ALL)
                logging.info(f"[INFO] Une interaction est en cours dans le serveur")
                async with message.channel.typing():
                    await asyncio.sleep(2)
                    response = nlp.get_answer(message.content)
                    await message.reply(response)
                return
            except Exception as e:
                await message.reply("Désolé, une erreur s'est produite lors du traitement de votre demande")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors d'une interaction dans le serveur : {e}" + Style.RESET_ALL)
                logging.error(f"[ERROR] Une erreur s'est produite lors d'une interaction dans le serveur : {e}")
        
        if channel_id in settings.TRAINING_CHANNEL_ID:
            keyword = settings.TRAINING_TRIGGER
            channel = bot.get_channel(settings.ALERT_CHANNEL)
            if content.endswith("?") or any(keyword in message.content for keyword in keyword):
                TEMP_QR[channel_id] = {"question": content, "user_id": message.author.id}
            elif channel_id in TEMP_QR:
                try:
                    prev = TEMP_QR[channel_id]
                    if message.reference:
                        save_suggestion(prev["question"], content)
                        del TEMP_QR[channel_id]
                        if channel is not None and isinstance(channel, discord.TextChannel):
                            await channel.send(f"```CAPTURE A VALIDER ENREGISTREE```")
                        print(Fore.WHITE + f"[DATA] Q/R capturée. En attente de validation." + Style.RESET_ALL)
                        logging.info(f"[DATA] Q/R capturée. En attente de validation.")
                except Exception as e:
                    if channel is not None and isinstance(channel, discord.TextChannel):
                        await channel.send(f"```LA CAPTURE A ECHOUEE: {e}```")
                    print(Fore.RED + f"[ERROR] Un erreur de capture de Q/R s'est produite : {e}" + Style.RESET_ALL)
                    logging.error(f"[ERROR] Un erreur de capture de Q/R s'est produite : {e}")

        await bot.process_commands(message)

        

    @bot.tree.command(name="restart", description="Redémarrer le bot.")
    async def restart(interaction: discord.Interaction):
        if not interaction.user.id in settings.ROOT_UER:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}")
            return
        try:
            client = bot.user
            await interaction.response.send_message(f"🔄 {client.name} va redémarrer...", ephemeral=False)
            print(Fore.MAGENTA + f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}")
            await bot.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur s'est produite lors du redémarrage : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}"+ Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}")
            return
    
    @bot.tree.command(name="commit", description="Enregistrer des informations dans le cloud.")
    async def commit(interaction: discord.Interaction, context: str, answer: str):
        """
        :param interaction: L'interaction Discord.
        :param context: Le context a associé à l'answer.
        :param answer: L'answer qui sera associé au context.
        """
        if not interaction.user.id in settings.ROOT_UER:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de commit : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de commit : {interaction.user.name}")
            return
        try:
            question = context
            reponse = answer
            with open(settings.KNOWLEDGE_PATH, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append({"question": question, "reponse": reponse})
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.truncate()
            await interaction.response.send_message("L'information a bien été commitée dans la base de connaissance.", ephemeral=True)
            print(Fore.GREEN + f"[INFO] Une information a été commitée par {interaction.user.name}" + Style.RESET_ALL)
            logging.info(f"[INFO] Une information: {question} a été commitée par {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors du commit : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du commit : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du commit : {e}")

    @bot.tree.command(name="empty", description="Vider le logging et le buffer.")
    async def empty(interaction: discord.Interaction):
        if not interaction.user.id in settings.ROOT_UER:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs et q/r : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs et q/r : {interaction.user.name}")
            return
        files_to_clear = {
            "Log File": settings.LOG_FILE,
            "Captured QR File": settings.CAPTURE_QR_PATH,
        }
        errors = []
        for file_name, file_path in files_to_clear.items():
            try:
                if not os.path.exists(file_path):
                    errors.append(f"{file_name} n'existe pas.")
                    continue
                with open(file_path, "w", encoding="utf-8") as file:
                    if file_name == "Captured QR File":
                        json.dump([], file, indent=2, ensure_ascii=False)
                    else:
                        file.write("")
                print(Fore.GREEN + f"[INFO] {file_name} a été vidé." + Style.RESET_ALL)
                logging.info(f"[INFO] {file_name} a été vidé. Demandé par {interaction.user.name}")
            except Exception as e:
                errors.append(f"Erreur lors du vidage de {file_name} : {e}")
                logging.error(f"[ERROR] Erreur lors du vidage de {file_name} : {e}")
        if errors:
            error_message = "\n".join(errors)
            await interaction.response.send_message(f"Des erreurs se sont produites :\n{error_message}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Des erreurs se sont produites :{error_message}" + Style.RESET_ALL)
        else:
            await interaction.response.send_message("Tous les fichiers ont été vidés avec succès.", ephemeral=True)
            print(Fore.GREEN + f"[INFO] Tous les fichiers ont été vidés avec succès." + Style.RESET_ALL)
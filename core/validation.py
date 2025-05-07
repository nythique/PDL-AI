from colorama import Fore, Style
from config import settings
import discord, json, logging

SUGGESTION_FILE = settings.CAPTURE_QR_PATH
KNOWLEDGE_FILE = settings.KNOWLEDGE_PATH

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_suggestions():
    try:
        print(Fore.CYAN + f"[INFO] Chargement de captured_qr.json\n")
        logging.info(f"[INFO] Chargement de captured_qr.json\n")
        with open(SUGGESTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Le chargement de captured_qr.json a échoué : {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] Le chargement de captured_qr.json a échoué : {e}")

def save_suggestions(data):
    try:
        print(Fore.CYAN + f"[INFO] Sauvegarde de captured_qr.json\n")
        logging.info(f"[INFO] Sauvegarde de captured_qr.json\n")
        with open(SUGGESTION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(Fore.RED + f"[ERROR] La sauvegarde de captured_qr.json a échoué {e}" + Style.RESET_ALL)
        logging.error(f"[ERROR] La sauvegarde de captured_qr.json a échoué {e}")

def add_to_knowledge(q, r):
    try:
        print(Fore.CYAN + f"[INFO] Téleversement de la sauvegarde dans knowledge\n" + Style.RESET_ALL)
        logging.info(f"[INFO] Téleversement de la sauvegarde dans knowledge\n")
        with open(KNOWLEDGE_FILE, "r+", encoding="utf-8") as f:
            knowledge = json.load(f)
            knowledge.append({"question": q, "reponse": r})
            f.seek(0)
            json.dump(knowledge, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Le téleversement de la sauvegarde a échoué" + Style.RESET_ALL)
        logging.error(f"[ERROR] Le téleversement de la sauvegarde a échoué")

def register_validation(bot):
    @bot.tree.command(name="push", description="Pousser captured_qr(collector) dans knowledge(data)")
    async def push(interaction: discord.Interaction):
        try:
            if not interaction.user.id in settings.ROOT_UER:
                await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
                print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de push : {interaction.user.name}" + Style.RESET_ALL)
                logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de push : {interaction.user.name}")
                return
            suggestions = load_suggestions()
            if not suggestions:
                await interaction.response.send_message("Aucun enregistrement de données à sauvegarder.", ephemeral=True)
                print(Fore.YELLOW + f"[INFO] {interaction.user.name} Aucun enregistrement de données à sauvegarder." + Style.RESET_ALL)
                return
            for entry in suggestions:
                add_to_knowledge(entry["question"], entry["reponse"])
            save_suggestions([])
            await interaction.response.send_message(f"{len(suggestions)} Q/R ajoutées à la base.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur de validation s'est produite : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur de validation s'est produite : {e}"+ Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur de validation s'est produite : {e}")
            return

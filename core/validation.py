from colorama import Fore, Style
from config import settings
from tools.cleaner import peer_filter  as cleaner
from ia.nlp import HybridNLPEngine
import discord, json, logging

SUGGESTION_FILE = settings.CAPTURE_QR_PATH
KNOWLEDGE_FILE = settings.KNOWLEDGE_PATH
nlp = HybridNLPEngine()

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

def is_duplicate(question, knowledge):
    print(Fore.YELLOW + f"[INFO] Vérification de la question : {question}" + Style.RESET_ALL)
    logging.info(f"[INFO] Vérification de la question : {question}")
    return any(entry["question"].strip().lower() == question.strip().lower() for entry in knowledge)

def register_validation(bot):
    @bot.tree.command(name="push", description="Pousser le buffer dans le cloud.")
    async def push(interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            if not interaction.user.id in settings.ROOT_UER:
                await interaction.followup.send("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
                print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de push : {interaction.user.name}" + Style.RESET_ALL)
                logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de push : {interaction.user.name}")
                return
            suggestions = load_suggestions()
            if not suggestions:
                await interaction.followup.send("Aucun enregistrement de données à sauvegarder.", ephemeral=True)
                print(Fore.YELLOW + f"[INFO] {interaction.user.name} Aucun enregistrement de données à sauvegarder." + Style.RESET_ALL)
                return
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                knowledge = json.load(f)
            if not isinstance(knowledge, list):
                await interaction.followup.send("La base de connaissances est corrompue ou n'est pas une liste.", ephemeral=True)
                print(Fore.RED + "[ERROR] La base de connaissances n'est pas une liste !" + Style.RESET_ALL)
                logging.error("[ERROR] La base de connaissances n'est pas une liste !")
                return
            valid_count = 0
            for entry in suggestions:
                question = entry.get("question", "").strip()
                reponse = entry.get("reponse", "").strip()
                # Vérifier la validité et les doublons
                if cleaner(question, reponse, knowledge) and not is_duplicate(question, knowledge):
                    add_to_knowledge(question, reponse)
                    valid_count += 1
                #add_to_knowledge(entry["question"], entry["reponse"])
            save_suggestions([])
            if valid_count == 0:
                await interaction.followup.send("Aucune Q/R valide n'a été ajoutée à la base.", ephemeral=True)
                print(Fore.YELLOW + "[INFO] Aucune Q/R valide n'a été ajoutée à la base." + Style.RESET_ALL)
                logging.info("[INFO] Aucune Q/R valide n'a été ajoutée à la base.")
                return
            #await interaction.response.send_message(f"{len(suggestions)} Q/R ajoutées à la base.", ephemeral=True)
            await interaction.followup.send(f"{valid_count} Q/R ajoutées à la base après filtrage.", ephemeral=True)
            print(Fore.GREEN + f"[INFO] {valid_count} Q/R ajoutées à la base après filtrage." + Style.RESET_ALL)
            logging.info(f"[INFO] {valid_count} Q/R ajoutées à la base après filtrage.")
            global nlp
            nlp = HybridNLPEngine()
            print(Fore.CYAN + "[INFO] Base NLP rechargée après commit." + Style.RESET_ALL)
            logging.info("[INFO] Base NLP rechargée après commit.")
        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur de validation s'est produite : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur de validation s'est produite : {e}"+ Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur de validation s'est produite : {e}")
            return

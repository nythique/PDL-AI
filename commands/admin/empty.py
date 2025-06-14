import discord, logging, os
from discord.ext import commands
from discord import app_commands
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ROOT_USER
from colorama import Fore, Style

info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

class Empty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="empty", description="ROOT | Vider les fichiers de logs")
    async def empty(self, interaction: discord.Interaction):
        if interaction.user.id not in ROOT_USER:
            await interaction.response.send_message(
                "⛔ Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True
            )
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}")
            return

        files_to_clear = {
            "Log File (Sécurité)": SECURITY_LOG_PATH,
            "Log File (Erreur)": ERROR_LOG_PATH,
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
                logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'information à {interaction.user.name} : {e}")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'information à {interaction.user.name}" + Style.RESET_ALL)

async def setup(bot):
    await bot.add_cog(Empty(bot))
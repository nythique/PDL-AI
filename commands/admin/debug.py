import discord,  os, logging
from config.settings import SECURITY_LOG_PATH
from discord.ext import commands
from discord import app_commands
from config.settings import ERROR_LOG_PATH, ROOT_USER
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

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="debug", description="ROOT | Afficher les erreurs du bot")
    @app_commands.describe(lines="Nombre de lignes à afficher (défaut : 10)")
    async def debug(self, interaction: discord.Interaction, lines: int = 10):
        if interaction.user.id not in ROOT_USER:
            await interaction.response.send_message(
                "⛔ Vous n'avez pas l'autorisation d'utiliser cette commande.", ephemeral=True
            )
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {interaction.user.name}")
            return

        log_path = ERROR_LOG_PATH
        if not os.path.exists(log_path):
            await interaction.response.send_message("Le fichier de logs d'erreur n'existe pas.", ephemeral=True)
            return
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines_content = f.readlines()[-lines:]
            if not lines_content:
                await interaction.response.send_message("Aucune erreur trouvée dans les logs.", ephemeral=True)
                return
            msg = "".join(lines_content)[-1900:]
            embed = discord.Embed(
                title="Dernières erreurs du bot",
                description=f"```{msg}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(Fore.GREEN + f"[INFO] Logs d'erreur envoyés" + Style.RESET_ALL)
            logging.info(f"[INFO] Logs d'erreur envoyés à {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message("Erreur lors de la lecture des logs.", ephemeral=True)
            print(Fore.RED + f"[ERROR] Erreur lors de la lecture des logs" + Style.RESET_ALL)
            logging.error(f"[ERROR] Erreur lors de la lecture des logs : {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
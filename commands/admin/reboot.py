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

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @app_commands.command(name="restart", description="ROOT | Rédemarrage rapide")
    async def restart(self, interaction: discord.Interaction):
        if not interaction.user.id in ROOT_USER:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de redemarrer le bot : {interaction.user.name}")
            return
        try:
            client = self.bot.user
            await interaction.response.send_message(f"🔄 Rédemarrage en cours...", ephemeral=True)
            print(Fore.MAGENTA + f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Le processus de redémarrage est lancer pour {client.name}")
            await self.bot.close()
        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur s'est produite lors du redémarrage : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}"+ Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du redémarrage : {e}")
            return

async def setup(bot):
    await bot.add_cog(Restart(bot))
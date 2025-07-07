import discord, logging
from plugins.utils.pve import get_hardware_info
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ROOT_USER
from discord.ext import commands
from discord import app_commands

info = get_hardware_info()
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



class Host(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="host", description="ROOT | Visualiser les informations de l'hôte")
    async def host(self, interaction: discord.Interaction):
        if interaction.user.id not in ROOT_USER:
            await interaction.response.send_message(
                "⛔ Vous devez être administrateur du serveur pour utiliser cette commande.", ephemeral=True
            )
            logging.warning(f"[HOST SECURITY] Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}")
            return
        try:
            embed = discord.Embed(
                title="Hoster Monitoring",
                description=f"""```Utilisation CPU: {info['cpu_usage']}%\nUtilisation RAM: {info['ram_usage']}%\nUtilisation Disque: {info['disk_usage']}%\nNombre de GPUs: {len(info['gpus'])} détectées```""",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            logging.info(f"[HOST] Informations de l'hôte envoyées à {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[HOST] Erreur lors de l'affichage de l'hôte pour {interaction.user} ({interaction.user.id}): {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de l'affichage de l'hôte",
                description=f"```{e}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Host(bot))
import discord, logging
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ALERT_CHANNEL
from config.settings import OWNER_ID as ROOT_USER

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

logger = logging.getLogger('report')
logger.handlers = []
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.setLevel(logging.INFO)

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="USER | Signaler un bug ou une suggestion")
    @app_commands.describe(message="Décris ton problème ou ta suggestion")
    async def report(self, interaction: discord.Interaction, message: str):
        try:
            await interaction.response.send_message(
                "Merci pour ton rapport ! L'équipe a bien reçu ta demande.", ephemeral=True
            )
            report_embed = discord.Embed(
                title="Nouveau rapport",
                description=f"```{message}```",
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            report_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            report_embed.set_footer(
                text=f"Identifiant de {interaction.user.display_name}: {interaction.user.id}"
            )
            channel = self.bot.get_channel(ALERT_CHANNEL)
            if channel:
                await channel.send(embed=report_embed)
                logger.info(f"[REPORT] Rapport envoyé par {interaction.user} ({interaction.user.id}) dans {channel.id}")
            else:
                ADMIN_ID = ROOT_USER[1]
                admin = await self.bot.fetch_user(ADMIN_ID)
                await admin.send(embed=report_embed)
                logger.warning(f"[REPORT] Salon de rapport introuvable, rapport envoyé à l'admin {ADMIN_ID}")
        except Exception as e:
            logger.error(f"[REPORT] Erreur lors de l'envoi du rapport par {interaction.user} ({interaction.user.id}) : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de l'envoi du rapport. Veuillez rejoindre le support pour y remedier",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Report(bot))
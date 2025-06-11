import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, REPORT_CHANNEL_ID
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from home.plugin.pipeline import set_whitelisted_channel


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

class Set(commands.GroupCog, name="set"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="channel", description="Définir le salon run-code pour ce serveur")
    @app_commands.describe(channel="Salon run-code")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            if not member or not member.guild_permissions.administrator:
                logging.warning(f"[SET] Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id} pour /set channel")
                await interaction.response.send_message(
                    "⛔ Vous devez être administrateur du serveur pour utiliser cette commande.", ephemeral=True
                )
                return

            set_whitelisted_channel(interaction.guild.id, channel.id)
            await interaction.response.send_message(
                f"✅ Salon run-code pour ce serveur : {channel.mention}", ephemeral=True
            )
            logging.info(f"[SET] Salon {channel.id} whitelisté sur {interaction.guild.id} par {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[SET] Erreur lors du whitelist du salon sur {interaction.guild.id} : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de la configuration du salon."
                "\nAssurez-vous que le bot a les permissions nécessaires et que vous êtes administrateur."
                "\nSi le problème persiste, contactez le support.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="report", description="Envoyer un rapport ou signaler un problème à l'équipe")
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

            channel = self.bot.get_channel(REPORT_CHANNEL_ID)
            if channel:
                await channel.send(embed=report_embed)
                logging.info(f"[REPORT] Rapport envoyé par {interaction.user} ({interaction.user.id}) dans {channel.id}")
            else:
                ADMIN_ID = 1233020939898327092
                admin = await self.bot.fetch_user(ADMIN_ID)
                await admin.send(embed=report_embed)
                logging.warning(f"[REPORT] Salon de rapport introuvable, rapport envoyé à l'admin {ADMIN_ID}")
        except Exception as e:
            logging.error(f"[REPORT] Erreur lors de l'envoi du rapport par {interaction.user} ({interaction.user.id}) : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de l'envoi du rapport.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Set(bot))
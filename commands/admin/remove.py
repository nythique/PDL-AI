import discord, logging, time
from discord import app_commands
from discord.ext import commands
from config import settings
from plugins.utils.db import Database 
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ROOT_USER, ALERT_CHANNEL, SERVER_DB


db = Database(SERVER_DB)
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

class Remove(commands.GroupCog, name="remove"):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_is_admin(self, interaction: discord.Interaction) -> bool:
        member = interaction.user
        if isinstance(member, discord.Member):
            if member.guild_permissions.administrator:
                return True
        root_users = db.get_all_root_users()
        return member.id in root_users

    @app_commands.command(name="channel", description="ADMIN | Retirer un salon de la liste des salons autorisés")
    @app_commands.describe(channel="Salon à retirer")
    async def remove_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not await self.interaction_is_admin(interaction):
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return
        try:
            allowed_channels = db.get_allowed_channels()
            if channel.id in allowed_channels:
                allowed_channels.remove(channel.id)
                db.set_allowed_channels(allowed_channels)
                db.save_data()
                logging.info(f"[REMOVE] Salon retiré : {channel.name} (ID: {channel.id}) par {interaction.user}.")
                await interaction.response.send_message(f"Salon retiré : {channel.mention} (ID: {channel.id}) de la liste des salons autorisés.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Le salon {channel.mention} (ID: {channel.id}) n'est pas dans la liste des salons autorisés.", ephemeral=True)
        except Exception as e:
            logging.error(f"[REMOVE][ERROR] Erreur lors de la suppression du salon {channel.name} (ID: {channel.id}) : {e}")
            await interaction.response.send_message(f"Erreur lors de la suppression du salon : {e}", ephemeral=True)

    @app_commands.command(name="status", description="ADMIN | Retirer un statut de la liste des statuts du bot")
    @app_commands.describe(status="Statut à retirer (autocomplétion)")
    async def remove_status(self, interaction: discord.Interaction, status: str):
        if not await self.interaction_is_admin(interaction):
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return
        try:
            statuses = db.get_bot_status()
            if status in statuses:
                statuses.remove(status)
                db.set_bot_status(statuses)
                db.save_data()
                logging.info(f"[REMOVE] Statut retiré : {status} par {interaction.user}.")
                await interaction.response.send_message(f"Statut retiré : `{status}`\nListe actuelle : {statuses if statuses else 'Aucun statut.'}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Le statut n'est pas dans la liste.\nStatuts actuels : {statuses}", ephemeral=True)
        except Exception as e:
            logging.error(f"[REMOVE][ERROR] Erreur lors de la suppression du statut '{status}' : {e}")
            await interaction.response.send_message(f"Erreur lors de la suppression du statut : {e}", ephemeral=True)

    @remove_status.autocomplete("status")
    async def status_autocomplete(self, interaction: discord.Interaction, current: str):
        statuses = db.get_bot_status()
        return [
            app_commands.Choice(name=s, value=s)
            for s in statuses if current.lower() in s.lower()
        ][:25]

async def setup(bot):
    await bot.add_cog(Remove(bot))

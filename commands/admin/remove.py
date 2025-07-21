import discord, logging, time
from discord import app_commands
from discord.ext import commands
from config import settings
from home.core.main import db
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ROOT_USER, ALERT_CHANNEL, SERVER_DB

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
            if channel.id in db.get_allowed_channels():
                db.remove_allowed_channel(channel.id)
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

    @app_commands.command(name="root", description="ADMIN | Retirer un utilisateur root")
    @app_commands.describe(user="Utilisateur à retirer des root")
    async def remove_root(self, interaction: discord.Interaction, user: discord.User):
        if not await self.interaction_is_admin(interaction):
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return
        try:
            root_users = db.get_all_root_users()
            if user.id in root_users:
                db.remove_root_user(user.id)
                await interaction.response.send_message(f"{user.mention} retiré des root.", ephemeral=True)
                logging.info(f"[REMOVE ROOT] {user.id} retiré des root par {interaction.user} ({interaction.user.id})")
            else:
                await interaction.response.send_message(f"{user.mention} n'est pas root.", ephemeral=True)
        except Exception as e:
            logging.error(f"[REMOVE ROOT] Erreur lors du retrait de root : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors du retrait de l'utilisateur root.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Remove(bot))

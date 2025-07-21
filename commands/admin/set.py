import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ROOT_USER, ALERT_CHANNEL, SERVER_DB
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from home.core.main import db

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

    @app_commands.command(name="channel", description="ADMIN | Configurer les salons pris en charge")
    @app_commands.describe(channel="Salon ajouté")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            admin_perms = not member or not (member.guild_permissions.administrator or member.id in ROOT_USER)

            if admin_perms: 
                logging.warning(f"[SET] Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id} pour /set channel")
                await interaction.response.send_message(
                    "⛔ Vous devez être administrateur du serveur pour utiliser cette commande.", ephemeral=True
                )
                return

            db.add_allowed_channel(channel.id)
            await interaction.response.send_message(
                f"Salon de conversation {channel.mention} ajouté avec succès !", ephemeral=True
            )
            logging.info(f"[SET CHANNEL] Salon {channel.id} Ajouté avec succès sur {interaction.guild.id} par {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[SET CHANNEL] Erreur lors de l'ajout du salon {channel.id} sur {interaction.guild.id} par {interaction.user} ({interaction.user.id}) : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de la configuration du salon."
                "\nAssurez-vous que le bot a les permissions nécessaires et que vous êtes administrateur."
                "\nSi le problème persiste, contactez le support.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

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
                logging.info(f"[REPORT] Rapport envoyé par {interaction.user} ({interaction.user.id}) dans {channel.id}")
            else:
                ADMIN_ID = ROOT_USER[1]
                admin = await self.bot.fetch_user(ADMIN_ID)
                await admin.send(embed=report_embed)
                logging.warning(f"[REPORT] Salon de rapport introuvable, rapport envoyé à l'admin {ADMIN_ID}")
        except Exception as e:
            logging.error(f"[REPORT] Erreur lors de l'envoi du rapport par {interaction.user} ({interaction.user.id}) : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de l'envoi du rapport. Veuillez rejoindre le support pour y remedier",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="status", description="ADMIN | Définir le statut du bot")
    @app_commands.describe(message="Définir le statut du bot")
    async def status(self, interaction: discord.Interaction, message: str):
        member = interaction.guild.get_member(interaction.user.id)
        admin_perms = not member or not (member.guild_permissions.administrator or member.id in ROOT_USER)
        if admin_perms: 
            await interaction.response.send_message(
                "⛔ Vous devez être administrateur ou root du serveur pour utiliser cette commande.", ephemeral=True
            )
            logging.warning(f"[SET STATUS] Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}")
            return
            
        
        try:
            current_statuses = db.get_bot_status()
            
            if isinstance(current_statuses, list):
                if message not in current_statuses:
                    current_statuses.append(message)
                    db.set_bot_status(current_statuses)
                    await interaction.response.send_message(f"✅ Statut ajouté : {message}\nStatuts disponibles : {', '.join(current_statuses)}", ephemeral=True)
                else:
                    await interaction.response.send_message(f"⚠️ Ce statut existe déjà : {message}", ephemeral=True)
            else:
                new_statuses = [current_statuses, message] if current_statuses != message else [message]
                db.set_bot_status(new_statuses)
                await interaction.response.send_message(f"✅ Statut défini : {message}\nStatuts disponibles : {', '.join(new_statuses)}", ephemeral=True)
            
            logging.info(f"[STATUS] Statut du bot défini par {interaction.user} ({interaction.user.id}) : {message}")
        except Exception as e:
            logging.error(f"[STATUS] Erreur lors de la définition du statut du bot par {interaction.user} ({interaction.user.id}) : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="```❌ Une erreur est survenue lors de la définition du statut du bot.```",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="root", description="ADMIN | Ajouter un utilisateur root")
    @app_commands.describe(user="Utilisateur à ajouter comme root")
    async def root(self, interaction: discord.Interaction, user: discord.User):
        member = interaction.guild.get_member(interaction.user.id)
        admin_perms = not member or not (member.guild_permissions.administrator or member.id in ROOT_USER)
        if admin_perms:
            await interaction.response.send_message(
                "⛔ Vous devez être administrateur ou root du serveur pour utiliser cette commande.", ephemeral=True
            )
            logging.warning(f"[SET ROOT] Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}")
            return
        try:
            db.add_root_user(user.id)
            await interaction.response.send_message(f"{user.mention} ajouté comme root.", ephemeral=True)
            logging.info(f"[SET ROOT] {user.id} ajouté comme root par {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[SET ROOT] Erreur lors de l'ajout de root : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de l'ajout de l'utilisateur root.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Set(bot))
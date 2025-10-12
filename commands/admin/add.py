# ==================================================================================
# ========================== GESTION MEMOIRE DU BOT DISCORD ========================
# ==================================================================================    
# Auteur: @NYTHIQUE
# GitHub: https://github.com/Nythique
# Porfolio: https://nythique.github.io
# Description: Ce fichier contient le code principal du bot Discord PDL-IA.
# Date de création: 01/05/2020
# Licence: GNU AFFERO GENERAL PUBLIC LICENSE
# ==================================================================================
# ========================= IMPORTATIONS ===========================================
import discord
import logging
from datetime import datetime
from home.core.main import db
from discord.ext import commands
from discord import app_commands
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, ALERT_CHANNEL, OWNER_ID

#======================================================================================
# ================= INITIALISATION DES PARAMETRES DE LOGGING ==========================

logger = logging.getLogger('database')
logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(
    SECURITY_LOG_PATH,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(
    ERROR_LOG_PATH,
    encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.handlers = []
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# ======================================================================================
# ======================= COGS DE LA CMD D'AJOUT  DES DONNEES ==========================

class Set(commands.GroupCog, name="add"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="channel", description="[ADMIN] | Ajouter un salon autorisé pour les conversations.")
    @app_commands.describe(channel="Salon à ajouter")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            authorization = (member.guild_permissions.administrator or member.id in db.selectData("adminList"))

            if not authorization: 
                await interaction.response.send_message(
                    "Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True
                )
                logger.warning(f"[WARNING ADD]-> Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}.")
                return
            else:
                db.addChannelList(channel.id)
                await interaction.response.send_message(
                    f"Je vais désormais répondre aux messages dans {channel.mention}.", ephemeral=True
                )
                logger.info(f"[SUCCÈS ADD]-> Salon {channel.id} ajouté avec succès sur {interaction.guild.id} par {interaction.user}.")
        except Exception as e:
            logger.error(f"[ERROR ADD]-> {e}, ligne 73.")
            await interaction.response.send_message(f"Une erreur critique s'est produite. Veulliez le signaler svp (/help).", ephemeral=True)

    @app_commands.command(name="status", description="[ADMIN] | Ajouter un statut au bot.")
    @app_commands.describe(message="Statut à ajouter au bot")
    async def status(self, interaction: discord.Interaction, message: str):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            if member.id not in db.selectData("adminList"): 
                await interaction.response.send_message(
                    "Cette commande est réservée aux administrateurs du bot.", ephemeral=True
                )
                logger.warning(f"[INFO ADD]-> Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}")
                return
        except Exception as e:
            logger.error(f"[ERROR ADD]-> {e}, ligne 88.")
            await interaction.response.send_message(
                "Une erreur critique s'est produite. Veulliez le signaler svp (/help).", ephemeral=True
            )
            return    
        
        try:
            currentStatuses = db.selectData("botStatusList") 
            if isinstance(currentStatuses, list):
                if message not in currentStatuses:
                    db.addBotStatusList(message)
                    await interaction.response.send_message(f"Merci ! Le nouveau statut **{message}** a été ajouté", ephemeral=True)
                    logger.info(f"[SUCCÈS ADD]-> Nouveau statut ajouté par {interaction.user} ({interaction.user.id}) : {message}")
                    return
                else:
                    await interaction.response.send_message(f"Désolé, le statut **{message}** existe déjà.", ephemeral=True)
                    logger.info(f"[SUCCÈS ADD]-> Le statut {message} existe déjà, ajouté par {interaction.user} ({interaction.user.id})")   
                    return
            else:
                newStatuses = [currentStatuses, message] if currentStatuses != message else [message]
                db.addBotStatusList(newStatuses)
                await interaction.response.send_message(f"Merci ! Le nouveau statut **{message}** a été ajouté", ephemeral=True)
                logger.info(f"[SUCCÈS ADD]-> Nouveau statut ajouté par {interaction.user} ({interaction.user.id}) : {message}")
                return
        except Exception as e:
            logger.error(f"[ERROR ADD]-> {e}, ligne 113.")
            await interaction.followup.send(f"Une erreur critique s'est produite. Veulliez le signaler svp (/help).", ephemeral=True)   

    @app_commands.command(name="admin", description="[OWNER] | Ajouter un administrateur du bot.")
    @app_commands.describe(user="Utilisateur à ajouter comme administrateur")
    async def admin(self, interaction: discord.Interaction, user: discord.User):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            if (member.id not in OWNER_ID) and (member.id not in db.selectData("adminList")):
                await interaction.response.send_message(
                    "Cette commande est réservée aux propriétaires et administrateur du bot.", ephemeral=True
                )
                logger.warning(f"[WARNING ADD]-> Accès refusé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id}.")
                return 
            else: 
                db.addAdminList(user.id)
                await interaction.response.send_message(f"L'utilisateur {user.mention} a été ajouté comme administrateur du bot.", ephemeral=True)
                logger.info(f"[SUCCÈS ADD]-> {user} ({user.id}) ajouté comme administrateur par {interaction.user} ({interaction.user.id}).") 
                return 
        except Exception as e:
            logger.error(f"[ERROR ADD]-> {e}, ligne 132.")
            await interaction.response.send_message(f"Une erreur critique s'est produite. Veulliez le signaler svp (/help).", ephemeral=True)
            return   

async def setup(bot):
    await bot.add_cog(Set(bot))
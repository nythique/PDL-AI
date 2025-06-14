import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands

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

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="help", description="USER | Consulter le menu d'aide du bot")
    async def help(self, interaction: discord.Interaction):
        try:
            bot_user = self.bot.user
            embed = discord.Embed(
                title="Aide de PDL IA",
                description="Voici les principales commandes et fonctionnalités du bot :",
                color=discord.Color.blue()
            )
            embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
            embed.add_field(name="/ping", value="Affiche la latence du bot et de Discord.", inline=False)
            embed.add_field(name="/set channel <salon>", value="Définir les salons pris en charge.", inline=False)
            embed.add_field(name="/set report <message>", value="Envoyer un rapport ou une suggestion à l'équipe.", inline=False)
            embed.add_field(name="/set status <message>", value="Définir le statut du bot.", inline=False)
            embed.add_field(name="/empty", value="Vider les logs de debug.", inline=False)
            embed.add_field(name="/restart", value="Redémarre le pdl-ia.", inline=False)
            embed.add_field(name="Interaction", value="Mentionne le bot ou utilise son nom pour discuter avec lui.", inline=False)
            embed.add_field(name="OCR", value="Envoie une image contenant du texte en DM ou sur le serveur pour que le bot l'analyse.", inline=False)
            embed.add_field(name="Musique", value="Demande moi de jouer une musique et je donnerai rendez-vous en voc.", inline=False)
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot&permissions=8"
            embed.add_field(
                name="Lien d'invitation",
                value=f"[Clique ici pour inviter PDL-IA sur ton serveur]({invite_url})",
                inline=False
            )
            embed.set_thumbnail(url=bot_user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info(f"[HELP] Message d'aide envoyé à {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[HELP] Erreur lors de l'affichage de l'aide pour {interaction.user} ({interaction.user.id}): {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de l'affichage de l'aide",
                description="❌ Une erreur est survenue lors de l'affichage de l'aide. Veuillez réessayer plus tard."
                "\nSi le problème persiste, contactez le support.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
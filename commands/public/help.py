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

    @app_commands.command(name="help", description="Afficher l'aide du bot")
    async def help(self, interaction: discord.Interaction):
        try:
            bot_user = self.bot.user
            embed = discord.Embed(
                title="Aide de PyLauncher",
                description="Voici les principales commandes et fonctionnalités du bot :",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=bot_user.display_avatar.url)
            embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
            embed.add_field(name="/ping", value="Affiche la latence du bot et de Discord.", inline=False)
            embed.add_field(name="/profil", value="Voir le profil du serveur et ses stats d'utilisation.", inline=False)
            embed.add_field(name="/set channel <salon>", value="Définir le salon autorisé pour ce serveur (admin requis).", inline=False)
            embed.add_field(name="/set report <message>", value="Envoyer un rapport ou une suggestion à l'équipe.", inline=False)
            embed.add_field(name="/notebook <titre> <code>", value="Génère un notebook Jupyter à partir de code Python.", inline=False)
            embed.add_field(name="/docs <sujet>", value="Consulte la documentation Python officielle (résumé en français).", inline=False)
            embed.add_field(name="/search <question>", value="Obtiens une réponse à une question Python.", inline=False)
            embed.add_field(name="/explain <code>", value="Donne une explication détaillée du code Python.", inline=False)
            embed.add_field(name="/transpile <langage> <code>", value="Convertit du code d'un autre langage vers Python.", inline=False)
            embed.add_field(name="/analyze <code>", value="Analyse le code Python pour détecter les erreurs.", inline=False)
            embed.add_field(name="/challenge <niveau> [sujet]", value="Génère un mini-problème Python adapté à ton niveau.", inline=False)
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot&permissions=8"
            embed.add_field(
                name="Lien d'invitation",
                value=f"[Clique ici pour inviter PyLauncher sur ton serveur]({invite_url})",
                inline=False
            )
            embed.set_footer(
                text="Développé par Nexium Portal • PyLauncher",
                icon_url=bot_user.display_avatar.url
            )
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

"""
   @bot.tree.command(name="help", description="Afficher l'aide du bot.")
    async def help(interaction: discord.Interaction):
        try:
            bot_user = bot.user
            embed = discord.Embed(
                title="Aide de PDL IA",
                description="Voici les principales commandes et fonctionnalités du bot :",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=bot_user.display_avatar.url)
            embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
            embed.add_field(name="/empty", value="Vider les fichiers logs", inline=False)
            embed.add_field(name="/restart", value="Redémarre le bot (admin seulement).", inline=False)
            embed.add_field(name="Préfix p.", value="errors <num>, voir les errors du logging", inline=False)
            embed.add_field(name="Préfix p.", value="ping , voir la latence du bot", inline=False)
            embed.add_field(name="Interaction", value="Mentionne le bot ou utilise son nom pour discuter avec lui.", inline=False)
            embed.add_field(name="OCR", value="Envoie une image contenant du texte en DM ou sur le serveur pour que le bot l'analyse.", inline=False)
            embed.set_footer(text="Développé par Nythique • PDL IA")
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot"
            embed.add_field(name="Lien d'invitation", value=f"[Clique ici pour inviter le bot]({invite_url})", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(Fore.GREEN + f"[INFO] Message d'aide envoyé à {interaction.user.name}" + Style.RESET_ALL)
            logging.info(f"[INFO] Message d'aide envoyé à {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de l'envoi de l'aide : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}")

"""
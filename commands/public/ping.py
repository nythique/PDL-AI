import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands
from datetime import datetime


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


class SlashUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="USER | Consulter le statut de latence")
    async def ping(self, interaction: discord.Interaction):
        try:
            ws_latency = round(self.bot.latency * 1000)
            color = discord.Color.green() if ws_latency < 100 else discord.Color.orange() if ws_latency < 250 else discord.Color.red()

            embed = discord.Embed(
                description=f"```Mon ping est de{ws_latency} ms.```",
                color=color,
                timestamp=datetime.now()
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
            embed.set_footer(
                text="PDL-IA • Propulsé par gg.PcPDL",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            logging.info(f"[PING] Pong envoyé à {interaction.user} ({interaction.user.id}) sur {interaction.guild.id if interaction.guild else 'DM'} ({ws_latency} ms)")
        except Exception as e:
            logging.error(f"[PING] Erreur lors de l'exécution de la commande ping : {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de l'exécution de la commande."
                "\nVeuillez réessayer plus tard ou contacter le support si le problème persiste.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashUtils(bot))
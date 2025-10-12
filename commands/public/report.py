"""
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
"""
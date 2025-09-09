import wavelink
import logging
from typing import Dict, Optional
from plugins.integrating.hosting.node_lavalink import LavalinkManager

logger = logging.getLogger("music")
logger.setLevel(logging.INFO)

info_handler = logging.FileHandler(settings.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(settings.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)
colorama.init()

class MusicPlayer:
    def __init__(self, lavalink_manager: LavalinkManager):
        self.lavalink = lavalink_manager
        self.guild_queues: Dict[int, list] = {}

    async def play_track(self, ctx, query: str):
        """Gestion de la lecture des pistes"""
        try:
            player = await self.lavalink.get_player(ctx.guild.id)
            if not player:
                await ctx.send("Impossible de se connecter au serveur de musique.")
                return

            if not player.is_connected:
                try:
                    await player.connect(ctx.author.voice.channel)
                except AttributeError:
                    await ctx.send("Vous devez être dans un salon vocal!")
                    return

            # Initialise la file d'attente si nécessaire
            if ctx.guild.id not in self.guild_queues:
                self.guild_queues[ctx.guild.id] = []

            tracks = await wavelink.YouTubeTrack.search(query)
            if not tracks:
                await ctx.send("Aucune musique trouvée.")
                return

            track = tracks[0]
            if player.is_playing():
                self.guild_queues[ctx.guild.id].append(track)
                await ctx.send(f"Ajouté à la file d'attente: {track.title}")
            else:
                await player.play(track)
                await ctx.send(f"Lecture en cours: {track.title}")

        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors de la lecture: {e}")
            await ctx.send("Une erreur s'est produite lors de la lecture.")

    async def handle_track_end(self, player: wavelink.Player):
        """Gestion de la fin des pistes"""
        guild_id = player.guild.id
        if guild_id in self.guild_queues and self.guild_queues[guild_id]:
            next_track = self.guild_queues[guild_id].pop(0)
            await player.play(next_track)
        else:
            await player.disconnect()
            if guild_id in self.guild_queues:
                del self.guild_queues[guild_id]

    # Méthodes de contrôle
    async def stop(self, ctx):
        player = await self.lavalink.get_player(ctx.guild.id)
        if player and player.is_playing():
            await player.stop()
            self.guild_queues[ctx.guild.id].clear()
            await ctx.send("Musique arrêtée.")

    async def pause(self, ctx):
        player = await self.lavalink.get_player(ctx.guild.id)
        if player and player.is_playing():
            await player.pause()
            await ctx.send("Musique en pause.")

    async def resume(self, ctx):
        player = await self.lavalink.get_player(ctx.guild.id)
        if player and player.is_paused:
            await player.resume()
            await ctx.send("Lecture reprise.")

    async def set_volume(self, ctx, volume: int):
        player = await self.lavalink.get_player(ctx.guild.id)
        if player:
            await player.set_volume(volume)
            await ctx.send(f"Volume réglé à {volume}%")
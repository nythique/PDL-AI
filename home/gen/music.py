import logging
import asyncio
import wavelink
import colorama

from typing import Dict, Optional
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from plugins.integrating.hosting.node_lavalink import LavalinkManager


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
colorama.init()

class MusicPlayer:
    def __init__(self, lavalink_manager):
        self.lavalink = lavalink_manager
        self.guild_queues: Dict[int, list] = {}
        self.volume_levels: Dict[int, int] = {}  

    async def _ensure_voice(self, ctx) -> bool:
        if not ctx.author.voice:
            await ctx.send("Vous devez être dans un salon vocal!")
            return False
        
        player = await self.lavalink.get_player(ctx.guild.id)
        if not player:
            await ctx.send("Impossible de se connecter au serveur de musique.")
            return False

        if not player.is_connected:
            try:
                await player.connect(ctx.author.voice.channel)
            except Exception as e:
                logging.error(f"[MUSIC] Erreur de connexion au salon vocal: {e}")
                await ctx.send("Impossible de rejoindre le salon vocal.")
                return False

        return True

    async def play_music(self, ctx, query: str):
        """Gestion de la lecture musicale"""
        try:
            if not await self._ensure_voice(ctx):
                return

            player = await self.lavalink.get_player(ctx.guild.id)
            if not player:
                return

            # Initialisation de la file d'attente si nécessaire
            if ctx.guild.id not in self.guild_queues:
                self.guild_queues[ctx.guild.id] = []
                self.volume_levels[ctx.guild.id] = 100

            # Recherche de la piste
            try:
                tracks = await wavelink.YouTubeTrack.search(query)
                if not tracks:
                    await ctx.send("Aucune musique trouvée.")
                    return

                track = tracks[0]
            except Exception as e:
                logging.error(f"[MUSIC] Erreur de recherche: {e}")
                await ctx.send("Erreur lors de la recherche de la musique.")
                return

            # Gestion de la lecture
            if player.is_playing():
                self.guild_queues[ctx.guild.id].append(track)
                await ctx.send(f"Ajouté à la file d'attente: {track.title}")
            else:
                await player.play(track)
                await player.set_volume(self.volume_levels[ctx.guild.id])
                await ctx.send(f"Lecture en cours: {track.title}")

        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors de la lecture: {e}")
            await ctx.send("Une erreur s'est produite lors de la lecture.")

    async def stop_music(self, ctx):
        """Arrête la musique et vide la file d'attente"""
        try:
            player = await self.lavalink.get_player(ctx.guild.id)
            if player and player.is_playing():
                self.guild_queues[ctx.guild.id].clear()
                await player.stop()
                await ctx.send("Musique arrêtée.")
            else:
                await ctx.send("Aucune musique en cours de lecture.")
        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors de l'arrêt: {e}")

    async def pause_music(self, ctx):
        """Met en pause la lecture"""
        try:
            player = await self.lavalink.get_player(ctx.guild.id)
            if player and player.is_playing():
                await player.pause()
                await ctx.send("Musique en pause.")
            else:
                await ctx.send("Aucune musique en cours de lecture.")
        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors de la pause: {e}")

    async def resume_music(self, ctx):
        """Reprend la lecture"""
        try:
            player = await self.lavalink.get_player(ctx.guild.id)
            if player and player.is_paused:
                await player.resume()
                await ctx.send("Lecture reprise.")
            else:
                await ctx.send("La musique n'est pas en pause.")
        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors de la reprise: {e}")

    async def set_volume(self, ctx, volume: int):
        """Règle le volume"""
        try:
            if not 0 <= volume <= 100:
                await ctx.send("Le volume doit être entre 0 et 100.")
                return

            player = await self.lavalink.get_player(ctx.guild.id)
            if player:
                await player.set_volume(volume)
                self.volume_levels[ctx.guild.id] = volume
                await ctx.send(f"Volume réglé à {volume}%")
            else:
                await ctx.send("Aucune lecture en cours.")
        except Exception as e:
            logging.error(f"[MUSIC] Erreur lors du réglage du volume: {e}")

    async def show_queue(self, ctx):
        """Affiche la file d'attente"""
        if ctx.guild.id not in self.guild_queues or not self.guild_queues[ctx.guild.id]:
            await ctx.send("La file d'attente est vide.")
            return

        queue = self.guild_queues[ctx.guild.id]
        queue_text = "\n".join([f"{i+1}. {track.title}" for i, track in enumerate(queue)])
        await ctx.send(f"File d'attente :\n{queue_text}")

    async def handle_track_end(self, player: wavelink.Player):
        """Gestion de la fin d'une piste"""
        guild_id = player.guild.id
        if guild_id in self.guild_queues and self.guild_queues[guild_id]:
            next_track = self.guild_queues[guild_id].pop(0)
            await player.play(next_track)
            await player.set_volume(self.volume_levels[guild_id])
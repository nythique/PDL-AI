import discord, logging, colorama, os, lavalink
from colorama import Fore, Style
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from typing import Optional, List, cast

logger = logging.getLogger("music")
logger.setLevel(logging.INFO)

if not logger.handlers:
    info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
    info_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
    error_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

colorama.init()

class LavalinkManager:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.node = None
        self.queues = {}

    async def setup_lavalink(self):
        try:
            # Configuration du nœud Lavalink
            node = lavalink.Node(
                uri=f"http://{os.getenv('LAVALINK_HOST', 'lavalink')}:{os.getenv('LAVALINK_PORT', '2333')}",
                password=os.getenv('LAVALINK_PASSWORD', 'youshallnotpass')
            )
            
            # Connexion au nœud
            await node.connect(client=self.bot)
            self.node = node
            
            logger.info("[lavalink] Connecté au serveur Lavalink")
            print(Fore.GREEN + "[lavalink] Connecté au serveur Lavalink" + Style.RESET_ALL)
            
        except Exception as e:
            logger.error(f"[lavalink] Erreur de connexion: {e}")
            print(Fore.RED + f"[lavalink] Erreur de connexion: {e}" + Style.RESET_ALL)

    async def on_lavalink_node_ready(self, payload) -> None:
        logger.info(f"[lavalink] Nœud {payload.node} prêt! Résumé: {payload.resumed}")

    async def on_lavalink_track_end(self, payload) -> None:
        try:
            player = payload.player
            if not player:
                return
                
            guild_id = player.guild.id
            if guild_id in self.queues and self.queues[guild_id]:
                next_track = self.queues[guild_id].pop(0)
                await self.play_track(guild_id, next_track)
        except Exception as e:
            logger.error(f"[lavalink] Erreur fin de piste: {e}")

    def get_player(self, guild_id: int):
        return self.players.get(guild_id)

    async def join_voice_channel(self, voice_channel: discord.VoiceChannel) -> bool:
        try:
            # Utiliser la classe Player de lavalink.py
            player = await voice_channel.connect(cls=lavalink.Player)
            self.players[voice_channel.guild.id] = player
            
            # Configuration du player
            player.autoplay = lavalink.AutoPlayMode.disabled
            player.home = voice_channel.guild.system_channel or voice_channel.guild.text_channels[0]
            
            logger.info(f"[lavalink] Connecté au salon: {voice_channel.name}")
            return True
        except Exception as e:
            logger.error(f"[lavalink] Erreur de connexion: {e}")
            print(Fore.RED + f"[lavalink] Erreur de connexion: {e}" + Style.RESET_ALL)
            return False

    async def search_track(self, query: str):
        try:
            # Recherche avec lavalink.py
            tracks = await lavalink.Playable.search(query)
            if tracks and len(tracks) > 0:
                return tracks[0]
            return None
        except Exception as e:
            logger.error(f"[lavalink] Erreur de recherche: {e}")
            print(Fore.RED + f"[lavalink] Erreur de recherche: {e}" + Style.RESET_ALL)
            return None

    async def play_track(self, guild_id: int, track) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                # Lecture avec lavalink.py
                await player.play(track)
                # Définir le volume après la lecture
                await player.set_volume(30)
                logger.info(f"[lavalink] Lecture: {track.title}")
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur de lecture: {e}")
            print(Fore.RED + f"[lavalink] Erreur de lecture: {e}" + Style.RESET_ALL)
            return False

    async def stop_playback(self, guild_id: int) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                await player.stop()
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur d'arrêt: {e}")
            print(Fore.RED + f"[lavalink] Erreur d'arrêt: {e}" + Style.RESET_ALL)
            return False

    async def pause_playback(self, guild_id: int) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                await player.pause(True)
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur de pause: {e}")
            print(Fore.RED + f"[lavalink] Erreur de pause: {e}" + Style.RESET_ALL)
            return False

    async def resume_playback(self, guild_id: int) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                await player.pause(False)
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur de reprise: {e}")
            print(Fore.RED + f"[lavalink] Erreur de reprise: {e}" + Style.RESET_ALL)
            return False

    async def set_volume(self, guild_id: int, volume: int) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                await player.set_volume(volume)
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur de volume: {e}")
            print(Fore.RED + f"[lavalink] Erreur de volume: {e}" + Style.RESET_ALL)
            return False

    async def disconnect(self, guild_id: int) -> bool:
        try:
            player = self.get_player(guild_id)
            if player:
                await player.disconnect()
                del self.players[guild_id]
                if guild_id in self.queues:
                    del self.queues[guild_id]
                return True
            return False
        except Exception as e:
            logger.error(f"[lavalink] Erreur de déconnexion: {e}")
            print(Fore.RED + f"[lavalink] Erreur de déconnexion: {e}" + Style.RESET_ALL)
            return False

    async def add_to_queue(self, guild_id: int, track) -> bool:
        try:
            if guild_id not in self.queues:
                self.queues[guild_id] = []
            self.queues[guild_id].append(track)
            return True
        except Exception as e:
            logger.error(f"[lavalink] Erreur d'ajout à la queue: {e}")
            return False

    def get_queue(self, guild_id: int) -> List:
        return self.queues.get(guild_id, [])

    def format_duration(self, duration_ms: int) -> str:
        seconds = int(duration_ms / 1000)
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def create_music_embed(self, title: str, description: str, color=discord.Color.blue()) -> discord.Embed:
        embed = discord.Embed(
            title=f"🎵 {title}",
            description=description,
            color=color
        )
        return embed
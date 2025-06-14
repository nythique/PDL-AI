import discord, logging, wavelink, colorama
#from wavelink.ext import spotify
from colorama import Fore, Style
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from typing import Optional

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

class WavelinkManager:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def setup_wavelink(self):
        node = wavelink.Node(
            uri='http://lavalink:2333',
            password='youshallnotpass'
        )
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])
        logging.info("[WAVELINK] Connecté au serveur Lavalink")
        print(Fore.GREEN + f"[WAVELINK] Connecté au serveur Lavalink"+ Style.RESET_ALL)

    async def get_player(self, guild_id: int) -> Optional[wavelink.Player]:
        if guild_id in self.players:
            return self.players[guild_id]
        return None

    async def join_voice_channel(self, voice_channel: discord.VoiceChannel) -> bool:
        try:
            player = await voice_channel.connect(cls=wavelink.Player)
            self.players[voice_channel.guild.id] = player
            logging.info(f"[WAVELINK] Connecté au salon: {voice_channel.name}")
            return True
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de connexion: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de connexion: {e}" + Style.RESET_ALL)
            return False

    async def search_track(self, query: str) -> Optional[wavelink.Playable]:
        try:
            tracks = await wavelink.Playable.search(query)
            if tracks:
                return tracks[0]
            return None
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de recherche: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de recherche: {e}" + Style.RESET_ALL)
            return None

    async def play_track(self, guild_id: int, track: wavelink.Track) -> bool:
        try:
            player = await self.get_player(guild_id)
            if player:
                await player.play(track)
                logging.info(f"[WAVELINK] Lecture: {track.title}")
                return True
            return False
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de lecture: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de lecture: {e}" + Style.RESET_ALL)
            return False

    async def stop_playback(self, guild_id: int) -> bool:
        try:
            player = await self.get_player(guild_id)
            if player:
                await player.stop()
                return True
            return False
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur d'arrêt: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur d'arrêt: {e}" + Style.RESET_ALL)
            return False

    async def pause_playback(self, guild_id: int) -> bool:
        try:
            player = await self.get_player(guild_id)
            if player:
                await player.pause()
                return True
            return False
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de pause: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de pause: {e}" + Style.RESET_ALL)
            return False

    async def resume_playback(self, guild_id: int) -> bool:
        try:
            player = await self.get_player(guild_id)
            if player:
                await player.resume()
                return True
            return False
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de reprise: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de reprise: {e}" + Style.RESET_ALL)
            return False

    async def set_volume(self, guild_id: int, volume: int) -> bool:
        try:
            player = await self.get_player(guild_id)
            if player:
                await player.set_volume(volume)
                return True
            return False
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur de volume: {e}")
            print(Fore.RED + f"[WAVELINK] Erreur de volume: {e}" + Style.RESET_ALL)
            return False

    async def get_player_info(self, guild_id: int) -> Optional[dict]:
        try:
            player = await self.players.get(guild_id)
            if player:
                return {
                    "track": player.track,
                    "is_playing": player.is_playing(),
                    "is_paused": player.is_paused(),
                    "volume": player.volume
                }
        except Exception as e:
            logging.error(f"[WAVELINK] Erreur {e}")
        return None

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
        embed.set_footer(text="Système Musical Lavalink • PDL Bot")
        return embed

    async def close(self):
        pass
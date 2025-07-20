import discord, logging, colorama, os, asyncio, random
from colorama import Fore, Style
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from typing import List, Dict, Optional
import yt_dlp

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

class MusicManager:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}  # {guild_id: voice_client}
        self.queues = {}   # {guild_id: [track_dict]}
        self.current_tracks = {}  # {guild_id: track_dict}
        self.default_volume = 0.5  # Volume par défaut (50%)

    def search_youtube(self, query: str) -> Optional[dict]:
        """Recherche une musique sur YouTube et retourne un dict avec titre, url, audio_url"""
        ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                video = info['entries'][0]
                return {
                    'title': video['title'],
                    'url': video['webpage_url'],
                    'audio_url': video['url']
                }
            except Exception as e:
                logger.error(f"[yt-dlp] Erreur de recherche: {e}")
                return None

    async def join_voice_channel(self, voice_channel: discord.VoiceChannel) -> bool:
        """Rejoint un salon vocal sans double connexion"""
        try:
            # Vérifie si déjà connecté au bon salon
            existing_client = discord.utils.get(self.bot.voice_clients, guild=voice_channel.guild)
            if existing_client:
                if existing_client.channel == voice_channel:
                    # Déjà connecté au bon salon
                    self.players[voice_channel.guild.id] = existing_client
                    logger.info(f"[yt] Déjà connecté au salon: {voice_channel.name}")
                    print(Fore.GREEN + f"[yt] Déjà connecté au salon: {voice_channel.name}" + Style.RESET_ALL)
                    return True
                else:
                    # Déjà connecté ailleurs, on déplace
                    await existing_client.move_to(voice_channel)
                    self.players[voice_channel.guild.id] = existing_client
                    logger.info(f"[yt] Déplacé dans le salon: {voice_channel.name}")
                    print(Fore.GREEN + f"[yt] Déplacé dans le salon: {voice_channel.name}" + Style.RESET_ALL)
                    return True
            # Sinon, on connecte normalement
            voice_client = await voice_channel.connect()
            self.players[voice_channel.guild.id] = voice_client
            logger.info(f"[yt] Connecté au salon: {voice_channel.name}")
            print(Fore.GREEN + f"[yt] Connecté au salon: {voice_channel.name}" + Style.RESET_ALL)
            return True
        except Exception as e:
            logger.error(f"[yt] Erreur de connexion: {e}")
            print(Fore.RED + f"[yt] Erreur de connexion: {e}" + Style.RESET_ALL)
            return False

    async def play_track(self, guild_id: int, query: str, volume: float = None) -> bool:
        """Joue une musique YouTube (par mot-clé ou lien)"""
        try:
            voice_client = self.players.get(guild_id)
            if not voice_client:
                logger.error(f"[yt] Aucun client vocal pour le serveur {guild_id}")
                return False

            # Arrêter la lecture actuelle si elle existe
            if voice_client.is_playing():
                voice_client.stop()

            # Recherche YouTube
            if query.startswith('http'):
                # Lien direct YouTube
                ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(query, download=False)
                    title = info.get('title', 'Inconnu')
                    audio_url = info['url']
                    url = info['webpage_url']
            else:
                # Recherche par mot-clé
                result = self.search_youtube(query)
                if not result:
                    logger.error(f"[yt] Aucun résultat pour: {query}")
                    return False
                title = result['title']
                audio_url = result['audio_url']
                url = result['url']

            # Créer la source audio avec volume
            if volume is None:
                volume = self.default_volume
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(audio_url, options='-vn'),
                volume=volume
            )

            # Lancer la lecture
            voice_client.play(source)
            self.current_tracks[guild_id] = {'title': title, 'url': url, 'audio_url': audio_url, 'volume': volume}
            logger.info(f"[yt] Lecture: {title}")
            print(Fore.GREEN + f"[yt] Lecture: {title}" + Style.RESET_ALL)
            return True
        except Exception as e:
            logger.error(f"[yt] Erreur de lecture: {e}")
            print(Fore.RED + f"[yt] Erreur de lecture: {e}" + Style.RESET_ALL)
            return False

    async def stop_playback(self, guild_id: int) -> bool:
        """Arrête la lecture"""
        try:
            voice_client = self.players.get(guild_id)
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                if guild_id in self.current_tracks:
                    del self.current_tracks[guild_id]
                return True
            return False
        except Exception as e:
            logger.error(f"[yt] Erreur d'arrêt: {e}")
            print(Fore.RED + f"[yt] Erreur d'arrêt: {e}" + Style.RESET_ALL)
            return False

    async def pause_playback(self, guild_id: int) -> bool:
        """Met en pause la lecture"""
        try:
            voice_client = self.players.get(guild_id)
            if voice_client and voice_client.is_playing():
                voice_client.pause()
                return True
            return False
        except Exception as e:
            logger.error(f"[yt] Erreur de pause: {e}")
            print(Fore.RED + f"[yt] Erreur de pause: {e}" + Style.RESET_ALL)
            return False

    async def resume_playback(self, guild_id: int) -> bool:
        """Reprend la lecture"""
        try:
            voice_client = self.players.get(guild_id)
            if voice_client and voice_client.is_paused():
                voice_client.resume()
                return True
            return False
        except Exception as e:
            logger.error(f"[yt] Erreur de reprise: {e}")
            print(Fore.RED + f"[yt] Erreur de reprise: {e}" + Style.RESET_ALL)
            return False

    async def set_volume(self, guild_id: int, volume: float) -> bool:
        """Définit le volume (0.0 à 1.0)"""
        try:
            voice_client = self.players.get(guild_id)
            if voice_client and voice_client.source:
                voice_client.source.volume = volume
                if guild_id in self.current_tracks:
                    self.current_tracks[guild_id]['volume'] = volume
                logger.info(f"[yt] Volume changé: {volume*100:.0f}%")
                return True
            return False
        except Exception as e:
            logger.error(f"[yt] Erreur de volume: {e}")
            print(Fore.RED + f"[yt] Erreur de volume: {e}" + Style.RESET_ALL)
            return False

    async def disconnect(self, guild_id: int) -> bool:
        """Se déconnecte du salon vocal"""
        try:
            voice_client = self.players.get(guild_id)
            if voice_client:
                await voice_client.disconnect()
                del self.players[guild_id]
                if guild_id in self.current_tracks:
                    del self.current_tracks[guild_id]
                if guild_id in self.queues:
                    del self.queues[guild_id]
                return True
            return False
        except Exception as e:
            logger.error(f"[yt] Erreur de déconnexion: {e}")
            print(Fore.RED + f"[yt] Erreur de déconnexion: {e}" + Style.RESET_ALL)
            return False

    async def add_to_queue(self, guild_id: int, query: str) -> bool:
        """Ajoute une musique à la queue (par mot-clé ou lien)"""
        try:
            if guild_id not in self.queues:
                self.queues[guild_id] = []
            self.queues[guild_id].append(query)
            return True
        except Exception as e:
            logger.error(f"[yt] Erreur d'ajout à la queue: {e}")
            return False

    def get_queue(self, guild_id: int) -> List[str]:
        """Retourne la queue d'un serveur"""
        return self.queues.get(guild_id, [])

    def get_current_track(self, guild_id: int) -> Optional[dict]:
        """Retourne la musique actuellement en cours"""
        return self.current_tracks.get(guild_id)

    def is_playing(self, guild_id: int) -> bool:
        """Vérifie si une musique est en cours de lecture"""
        voice_client = self.players.get(guild_id)
        return voice_client and voice_client.is_playing()

    def is_paused(self, guild_id: int) -> bool:
        """Vérifie si la musique est en pause"""
        voice_client = self.players.get(guild_id)
        return voice_client and voice_client.is_paused()

    def create_music_embed(self, title: str, description: str, color=discord.Color.blue()) -> discord.Embed:
        """Crée un embed pour les informations de musique"""
        embed = discord.Embed(
            title=f"🎵 {title}",
            description=description,
            color=color
        )
        return embed

    def get_queue_embed(self, guild_id: int) -> discord.Embed:
        """Crée un embed avec la liste des musiques dans la queue"""
        queue = self.get_queue(guild_id)
        embed = discord.Embed(
            title="🎵 File d'attente",
            description="Voici la file d'attente :",
            color=discord.Color.green()
        )
        for i, query in enumerate(queue, 1):
            embed.add_field(
                name=f"{i}.",
                value=f"{query}",
                inline=False
            )
        return embed
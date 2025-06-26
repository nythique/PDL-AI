import discord, logging, colorama, os, asyncio, random
from colorama import Fore, Style
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from typing import List, Dict, Optional
import glob

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

class LocalTrack:
    def __init__(self, file_path: str, title: str = None):
        self.file_path = file_path
        self.title = title or os.path.basename(file_path).replace('.mp3', '')
        self.duration = 0  

class MusicManager:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}  # {guild_id: voice_client}
        self.queues = {}   # {guild_id: [LocalTrack]}
        self.current_tracks = {}  # {guild_id: LocalTrack}
        self.audio_folder = "archive/audio"
        self.available_tracks = self._load_local_tracks()
        
    def _load_local_tracks(self) -> List[LocalTrack]:
        """Charge tous les fichiers audio disponibles"""
        tracks = []
        audio_pattern = os.path.join(self.audio_folder, "*.mp3")
        
        for file_path in glob.glob(audio_pattern):
            track = LocalTrack(file_path)
            tracks.append(track)
            
        logger.info(f"[local] {len(tracks)} pistes locales chargées")
        print(Fore.GREEN + f"[local] {len(tracks)} pistes locales chargées" + Style.RESET_ALL)
        return tracks
    
    def get_available_tracks(self) -> List[LocalTrack]:
        """Retourne la liste des pistes disponibles"""
        return self.available_tracks.copy()
    
    def search_track_by_name(self, query: str) -> Optional[LocalTrack]:
        """Recherche une piste par nom"""
        query_lower = query.lower()
        for track in self.available_tracks:
            if query_lower in track.title.lower():
                return track
        return None
    
    def get_random_track(self) -> Optional[LocalTrack]:
        """Retourne une piste aléatoire"""
        if self.available_tracks:
            return random.choice(self.available_tracks)
        return None

    async def join_voice_channel(self, voice_channel: discord.VoiceChannel) -> bool:
        """Rejoint un salon vocal"""
        try:
            voice_client = await voice_channel.connect()
            self.players[voice_channel.guild.id] = voice_client
            
            logger.info(f"[local] Connecté au salon: {voice_channel.name}")
            print(Fore.GREEN + f"[local] Connecté au salon: {voice_channel.name}" + Style.RESET_ALL)
            return True
            
        except Exception as e:
            logger.error(f"[local] Erreur de connexion: {e}")
            print(Fore.RED + f"[local] Erreur de connexion: {e}" + Style.RESET_ALL)
            return False

    async def play_track(self, guild_id: int, track: LocalTrack) -> bool:
        """Joue une piste locale"""
        try:
            voice_client = self.players.get(guild_id)
            if not voice_client:
                logger.error(f"[local] Aucun client vocal pour le serveur {guild_id}")
                return False
            
            # Arrêter la lecture actuelle si elle existe
            if voice_client.is_playing():
                voice_client.stop()
            
            # Créer la source audio
            audio_source = discord.FFmpegPCMAudio(
                track.file_path,
                options='-vn -b:a 192k'
            )
            
            # Lancer la lecture
            voice_client.play(audio_source)
            self.current_tracks[guild_id] = track
            
            logger.info(f"[local] Lecture: {track.title}")
            print(Fore.GREEN + f"[local] Lecture: {track.title}" + Style.RESET_ALL)
            return True
            
        except Exception as e:
            logger.error(f"[local] Erreur de lecture: {e}")
            print(Fore.RED + f"[local] Erreur de lecture: {e}" + Style.RESET_ALL)
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
            logger.error(f"[local] Erreur d'arrêt: {e}")
            print(Fore.RED + f"[local] Erreur d'arrêt: {e}" + Style.RESET_ALL)
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
            logger.error(f"[local] Erreur de pause: {e}")
            print(Fore.RED + f"[local] Erreur de pause: {e}" + Style.RESET_ALL)
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
            logger.error(f"[local] Erreur de reprise: {e}")
            print(Fore.RED + f"[local] Erreur de reprise: {e}" + Style.RESET_ALL)
            return False

    async def set_volume(self, guild_id: int, volume: int) -> bool:
        """Définit le volume (note: FFmpegPCMAudio ne supporte pas le changement de volume)"""
        try:
            # FFmpegPCMAudio ne supporte pas le changement de volume dynamique
            # Il faudrait utiliser discord.PCMVolumeTransformer pour cela
            logger.info(f"[local] Volume demandé: {volume}% (non supporté avec FFmpegPCMAudio)")
            return True
            
        except Exception as e:
            logger.error(f"[local] Erreur de volume: {e}")
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
            logger.error(f"[local] Erreur de déconnexion: {e}")
            print(Fore.RED + f"[local] Erreur de déconnexion: {e}" + Style.RESET_ALL)
            return False

    async def add_to_queue(self, guild_id: int, track: LocalTrack) -> bool:
        """Ajoute une piste à la queue"""
        try:
            if guild_id not in self.queues:
                self.queues[guild_id] = []
            self.queues[guild_id].append(track)
            return True
            
        except Exception as e:
            logger.error(f"[local] Erreur d'ajout à la queue: {e}")
            return False

    def get_queue(self, guild_id: int) -> List[LocalTrack]:
        """Retourne la queue d'un serveur"""
        return self.queues.get(guild_id, [])

    def get_current_track(self, guild_id: int) -> Optional[LocalTrack]:
        """Retourne la piste actuellement en cours"""
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

    def get_track_list_embed(self) -> discord.Embed:
        """Crée un embed avec la liste des pistes disponibles"""
        embed = discord.Embed(
            title="🎵 Musiques Locales Disponibles",
            description="Voici toutes les musiques disponibles :",
            color=discord.Color.green()
        )
        
        for i, track in enumerate(self.available_tracks, 1):
            embed.add_field(
                name=f"{i}. {track.title}",
                value=f"Fichier: `{os.path.basename(track.file_path)}`",
                inline=False
            )
        
        return embed
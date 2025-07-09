import os
import time
import logging
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
from config import settings
from config.settings import TEMP_UPLOAD_PATH
import asyncio
import tempfile
from pydub import AudioSegment


def setup_logger() -> None:
    """Configure les gestionnaires de logs pour info et erreur."""
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

    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

setup_logger()
logger = logging.getLogger(__name__)


def get_audio_path(user_id: str, who: str = "user", ext: str = "wav") -> str:
    """Génère un chemin de fichier audio temporaire unique."""
    timestamp = int(time.time() * 1000)
    folder = os.path.join(os.getcwd(), TEMP_UPLOAD_PATH)
    os.makedirs(folder, exist_ok=True)
    filename = f"{who}_{user_id}_{timestamp}.{ext}"
    path = os.path.join(folder, filename)
    logger.info(f"Chemin audio généré : {path}")
    return path


async def speech_to_text(file_path: str, lang: str = "fr-FR") -> Optional[str]:
    """Transcrit un fichier audio en texte (accepte mp3, wav, etc.)."""
    recognizer = sr.Recognizer()
    ext = os.path.splitext(file_path)[1].lower()
    temp_wav = None

    try:
        # Conversion si ce n'est pas déjà un wav
        if ext != ".wav":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio = AudioSegment.from_file(file_path)
                audio.export(tmp.name, format="wav")
                temp_wav = tmp.name
            file_to_process = temp_wav
        else:
            file_to_process = file_path

        def recognize():
            with sr.AudioFile(file_to_process) as source:
                audio = recognizer.record(source)
            try:
                # Utilisation de recognize_google si disponible, sinon lever une erreur explicite
                recognize_google = getattr(recognizer, "recognize_google", None)
                if not callable(recognize_google):
                    raise AttributeError("La méthode recognize_google n'est pas disponible dans la classe Recognizer.")
                return recognize_google(audio, language=lang)
            except AttributeError as e:
                logger.error(f"Erreur : {e}")
                return None

        text = await asyncio.get_event_loop().run_in_executor(None, recognize)
        if isinstance(text, str):
            logger.info(f"Transcription réussie pour {file_path}")
            return text
        else:
            return None
    except Exception as e:
        logger.error(f"Erreur de transcription pour {file_path} : {e}")
        return None
    finally:
        # Nettoyage du fichier temporaire si conversion
        if temp_wav and os.path.exists(temp_wav):
            os.remove(temp_wav)


async def text_to_speech(text: str, user_id: str, lang: str = "fr") -> Optional[str]:
    """Convertit du texte en audio (asynchrone)."""
    path = get_audio_path(user_id, who="bot", ext="mp3")
    try:
        def synthesize():
            tts = gTTS(text=text, lang=lang)
            tts.save(path)
        await asyncio.get_event_loop().run_in_executor(None, synthesize)
        logger.info(f"Synthèse vocale réussie pour {user_id}, fichier : {path}")
        return path
    except Exception as e:
        logger.error(f"Erreur de synthèse vocale pour {user_id} : {e}")
        return None
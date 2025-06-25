from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

class SpeechIO:
    @staticmethod
    def text_to_audio(text: str, output_path: str = "output.mp3", lang: str = "fr"):
        """Convertit du texte en fichier audio (MP3)."""
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path

    @staticmethod
    def audio_to_text(audio_path: str, lang: str = "fr-FR") -> str:
        """Convertit un fichier audio en texte."""
        recognizer = sr.Recognizer()
        # Conversion en wav si besoin
        if not audio_path.endswith(".wav"):
            sound = AudioSegment.from_file(audio_path)
            audio_path_wav = audio_path.rsplit('.', 1)[0] + ".wav"
            sound.export(audio_path_wav, format="wav")
        else:
            audio_path_wav = audio_path

        with sr.AudioFile(audio_path_wav) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language=lang)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Erreur API Google Speech: {e}")
            return ""
SpeechIO.text_to_audio("Bonjour", lang="fr")
#SpeechIO.audio_to_text("bonjour.mp3", lang="fr-FR")

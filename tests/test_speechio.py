import asyncio
from plugins.speechio import speech_to_text, text_to_speech
import os

# Chemin d'un fichier audio de test (à adapter selon ton environnement)
AUDIO_TEST_PATH = "home/cluster/temp/bot_testuser_1751493083136.mp3"  # Place un petit fichier wav ici pour tester

async def test_speech_to_text():
    print("Test de speech_to_text...")
    if not os.path.exists(AUDIO_TEST_PATH):
        print(f"Fichier audio de test non trouvé : {AUDIO_TEST_PATH}")
        return
    texte = await speech_to_text(AUDIO_TEST_PATH)
    print(f"Texte reconnu : {texte}")

async def test_text_to_speech():
    print("Test de text_to_speech...")
    texte = "Bonjour,moi je m'appelle PDL-AI, je suis l'assistante du serveur. J'ai été developpée par nythique et je suis administré par sanchaton et tintin. Je suis hebergée sur la vm de Paxou"
    user_id = "testuser"
    audio_path = await text_to_speech(texte, user_id)
    if audio_path and os.path.exists(audio_path):
        print(f"Fichier audio généré : {audio_path}")
    else:
        print("Erreur lors de la génération du fichier audio.")

if __name__ == "__main__":
    #asyncio.run(test_text_to_speech()) 
    asyncio.run(test_speech_to_text())
    
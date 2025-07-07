import pytesseract, os, logging, uuid
from PIL import Image
from config import settings
from colorama import Fore, Style

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

class OCRProcessor:
    def __init__(self, tesseract_path=None):

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.logger = logging.getLogger(__name__)

        # Vérifier et créer le répertoire d'upload si nécessaire
        if not os.path.exists(settings.TEMP_UPLOAD_PATH):
            os.makedirs(settings.TEMP_UPLOAD_PATH)
            print(Fore.GREEN + f"[INFO] Répertoire créé : {settings.TEMP_UPLOAD_PATH}" + Style.RESET_ALL)
            self.logger.info(f"Répertoire créé : {settings.TEMP_UPLOAD_PATH}")

    async def extract_text(self, image_path):
        """
        Extrait le texte d'une image donnée.
        :param image_path: Chemin de l'image à analyser.
        """
        try:
            
            image = Image.open(image_path)
            # Extraire le texte avec Tesseract
            extracted_text = pytesseract.image_to_string(image)
            print(Fore.GREEN + f"[INFO] Texte extrait avec succès depuis {image_path}" + Style.RESET_ALL)
            self.logger.info(f"Texte extrait avec succès depuis {image_path}")
            return extracted_text.strip()
        except Exception as e:
            print(Fore.RED + f"[ERROR] Erreur lors de l'analyse de l'image {image_path} : {e}" + Style.RESET_ALL)
            self.logger.error(f"Erreur lors de l'analyse de l'image {image_path} : {e}")
            raise e

    async def process_attachment(self, attachment):
        """
        Télécharge et analyse une pièce jointe Discord.     
        :param attachment: Pièce jointe Discord.
        """
        try:
            local_filename = os.path.join(settings.TEMP_UPLOAD_PATH, f"{uuid.uuid4()}_{attachment.filename}")
            await attachment.save(local_filename)
            print(Fore.CYAN + f"[INFO] Image téléchargée : {local_filename}" + Style.RESET_ALL)
            self.logger.info(f"Image téléchargée : {local_filename}")

            extracted_text = await self.extract_text(local_filename)
            return "Description de l'image:" + extracted_text if extracted_text else "❌ Aucun texte détecté dans l'image."
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Erreur lors du traitement de la pièce jointe : {e}" + Style.RESET_ALL)
            self.logger.error(f"Erreur lors du traitement de la pièce jointe : {e}")
            return f"❌ Une erreur s'est produite lors de l'analyse de l'image : {e}"
        finally:
            if os.path.exists(local_filename):
                try:
                    os.remove(local_filename)
                    print(Fore.YELLOW + f"[INFO] Fichier supprimé : {local_filename}" + Style.RESET_ALL)
                    self.logger.info(f"Fichier supprimé : {local_filename}")
                except Exception as e:
                    print(Fore.RED + f"[ERROR] Erreur lors de la suppression du fichier {local_filename} : {e}" + Style.RESET_ALL)
                    self.logger.error(f"Erreur lors de la suppression du fichier {local_filename} : {e}")
            
            
        
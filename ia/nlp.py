from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from ia.loader import load_knowledge
from config import settings
from cluster.vram import memory
from colorama import Fore, Style
import torch, logging, time

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HybridNLPEngine:
    def __init__(self):
        try:
            logging.info("[INFO] Chargement de la base de connaissances...")
            print(Fore.YELLOW + "[INFO] Chargement de la base de connaissances..." + Style.RESET_ALL)
            time.sleep(1)
            self.knowledge = load_knowledge(settings.KNOWLEDGE_PATH)
            if not self.knowledge:
                logging.warning("[WARNING] Aucune connaissance valide trouvée.")
                raise ValueError("La base de connaissances est vide ou invalide.")
            logging.info("[INFO] Initialisation des modèles TF-IDF et SBERT...")
            self.tfidf_vectorizer = TfidfVectorizer()
            self.sbert_model = SentenceTransformer(settings.SBERT_MODEL)
            self.questions = [item["question"] for item in self.knowledge]
            self.answers = [item["reponse"] for item in self.knowledge]
            self.tfidf_vectors = self.tfidf_vectorizer.fit_transform(self.questions)
            self.sbert_embeddings = self.sbert_model.encode(self.questions, convert_to_tensor=True)
            logging.info("[INFO] HybridNLPEngine initialisé avec succès.")
            print(Fore.GREEN + "[INFO] HybridNLPEngine initialisé avec succès." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'initialisation de HybridNLPEngine : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation de HybridNLPEngine : {e}" + Style.RESET_ALL)
            raise

    def get_answer(self, question):
        try:
            logging.info(f"[INFO] Question reçue : {question}")
            if not question.strip():
                logging.warning("[WARNING] Question vide reçue.")
                return "Je ne peux pas répondre à une question vide."
            
            tfidf_vector = self.tfidf_vectorizer.transform([question])
            tfidf_similarity = cosine_similarity(tfidf_vector, self.tfidf_vectors)
            best_tfidf_index = tfidf_similarity.argmax()
            best_tfidf_score = tfidf_similarity[0, best_tfidf_index]
            logging.info(f"[INFO] Score TF-IDF : {best_tfidf_score}")
            print(Fore.YELLOW + f"[INFO] Score TF-IDF : {best_tfidf_score}" + Style.RESET_ALL)

            if best_tfidf_score >= settings.SIMILARITY_IDF:
                logging.info(f"[INFO] Réponse trouvée avec TF-IDF : {self.answers[best_tfidf_index]}")
                print(Fore.GREEN + f"[INFO] Réponse trouvée avec TF-IDF : {self.answers[best_tfidf_index]}" + Style.RESET_ALL)
                return self.answers[best_tfidf_index]

            sbert_embedding = self.sbert_model.encode(question, convert_to_tensor=True)
            sbert_similarity = util.pytorch_cos_sim(sbert_embedding, self.sbert_embeddings)[0]
            best_sbert_index = torch.argmax(sbert_similarity).item()
            best_sbert_score = torch.max(sbert_similarity).item()
            logging.info(f"[INFO] Score SBERT : {best_sbert_score}")
            print(Fore.YELLOW + f"[INFO] Score SBERT : {best_sbert_score}" + Style.RESET_ALL)

            if best_sbert_score >= settings.SIMILARITY_SBERT:
                logging.info(f"[INFO] Réponse trouvée avec SBERT : {self.answers[best_sbert_index]}")
                print(Fore.GREEN + f"[INFO] Réponse trouvée avec SBERT : {self.answers[best_sbert_index]}" + Style.RESET_ALL)
                return self.answers[best_sbert_index]

            logging.warning("[WARNING] Aucune réponse pertinente trouvée.")
            print(Fore.RED + "[WARNING] Aucune réponse pertinente trouvée." + Style.RESET_ALL)
            return "Désolé, je ne suis pas sûr de la réponse à ta question."
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la recherche de réponse : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la recherche de réponse : {e}" + Style.RESET_ALL)
            return "Désolé, une erreur s'est produite lors de la recherche de la réponse."
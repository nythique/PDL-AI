from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import settings
from ia.loader import load_knowledge
import logging

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class NLPEngine:
    def __init__(self):
        try:
            logging.info("[INFO] Initialisation de NLPEngine...")
            self.knowledge = load_knowledge(settings.KNOWLEDGE_PATH)
            if not self.knowledge:
                logging.warning("[INFO] Aucune connaissance trouvée dans le fichier.")
                raise ValueError("Aucune connaissance trouvée dans le fichier.")
            self.questions = [entry["question"] for entry in self.knowledge]
            self.answers = [entry["reponse"] for entry in self.knowledge]
            self.vectorizer = TfidfVectorizer()
            self.vectors = self.vectorizer.fit_transform(self.questions)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'initialisation de NLPEngine: {e}")
            raise
        logging.info("[INFO] NLPEngine initialisé avec succès.")

    def get_answer(self, question):
        try:
            logging.info(f"[INFO] Une question reçue.")
            if not question:
                logging.warning(f"[WARNING] Question vide reçue: {question}")
                return "Je ne peux pas répondre à une question vide."
            vector = self.vectorizer.transform([question])
            similarity = cosine_similarity(vector, self.vectors)
            best_index = similarity.argmax()
            score = similarity[0, best_index]
            logging.info(f"[INFO] Similarité calculée: {score} pour la question: {question}")
            if score < settings.SIMILARITY_THRESHOLD:
                return "Je ne suis pas certain de comprendre. Peux-tu reformuler ?" or "Explique mieux ton soucis pour que je puisse le comprendre." 
            return self.answers[best_index]
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la recherche de réponse: {e}")
            return "Désolé, je n'ai pas pu trouver une réponse à ta question."
        

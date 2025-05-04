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
        self.knowledge = load_knowledge(settings.KNOWLEDGE_PATH)
        self.questions = [entry["question"] for entry in self.knowledge]
        self.answers = [entry["reponse"] for entry in self.knowledge]
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.questions)

    def get_answer(self, question):
        vector = self.vectorizer.transform([question])
        similarity = cosine_similarity(vector, self.vectors)
        best_index = similarity.argmax()
        score = similarity[0, best_index]
        if score < settings.SIMILARITY_THRESHOLD:
            return "Je ne suis pas certain de comprendre. Peux-tu reformuler ?" or "Explique mieux ton soucis pour que je puisse le comprendre." 
        return self.answers[best_index]

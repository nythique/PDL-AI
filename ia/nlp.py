from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from ia.loader import load_knowledge
from config import settings
from cluster.vram import memory
from colorama import Fore, Style
from groq import Groq
import torch, logging, time, PyPDF2

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HybridNLPEngine:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.KEY) 
        self.pdf_passages = []
        self.conversation_history = []
        try:
            print(Fore.CYAN + "[INFO] Chargement du PDF..." + Style.RESET_ALL)
            logging.info("[INFO] Chargement du PDF...")
            with open(settings.PDF_PATH, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        self.pdf_passages.extend([p.strip() for p in text.split('\n') if p.strip()])
            print(Fore.GREEN + "[INFO] Chargement du PDF terminé." + Style.RESET_ALL)
            logging.info("[INFO] Chargement du PDF terminé.")
            print(Fore.CYAN + f"[INFO] Nombre de lignes extraites du PDF : {len(self.pdf_passages)}" + Style.RESET_ALL)
            logging.info(f"[INFO] Nombre de lignes extraites du PDF : {len(self.pdf_passages)}")
        except Exception as e:
            logging.warning(f"[WARNING] Impossible de charger le PDF : {e}")
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

    def find_best_pdf_passage(self, question):
        if not self.pdf_passages:
            return ""
        vect = TfidfVectorizer().fit(self.pdf_passages + [question])
        tfidf = vect.transform(self.pdf_passages + [question])
        sims = cosine_similarity(tfidf[-1], tfidf[:-1])
        idx = sims.argmax()
        best = self.pdf_passages[idx]
        return best

    def get_answer(self, question):
        try:
            self.conversation_history.append({"role": "user", "content": question})
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
            
            # Si aucune réponse pertinente, fallback API
            logging.warning("[WARNING] Aucune réponse pertinente trouvée. Appel à l'API IA.")
            print(Fore.MAGENTA + "[INFO] Appel à l'API IA externe..." + Style.RESET_ALL)
            api_response = self.ask_api(question)
            return api_response
        
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la recherche de réponse : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la recherche de réponse : {e}" + Style.RESET_ALL)
            return "Désolé, une erreur s'est produite lors de la recherche de la réponse."
    
    def ask_api(self, question):
    
        try:
            # Ajoute la question courante à l'historique
            self.conversation_history.append({"role": "user", "content": question})
            # Prend les derniers échanges (user + assistant)
            history = self.conversation_history[-settings.LIMIT_MEMORY*2:]  # *2 car user+assistant
            #history = self.conversation_history[-settings.LIMIT_MEMORY:] if len(self.conversation_history) > settings.LIMIT_MEMORY else self.conversation_history[:]
            pdf_info = self.find_best_pdf_passage(question)
            system_prompt = (settings.PROMPT) + \
                            " Réponds de façon brève et précise. Si utile, utilise l'information suivante du document : " + pdf_info
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            #messages.append({"role": "user", "content": question})
            response = self.groq_client.chat.completions.create(
                model=settings.MODEL,
                messages=messages,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                top_p=settings.TOP_P,
                frequency_penalty=settings.FREQUENCY,
                presence_penalty=settings.PRESENCE_PENALTY,
                #stop=settings.STOP
            )
            # Ajouter la réponse à l'historique
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'appel à l'API IA : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'appel à l'API IA : {e}" + Style.RESET_ALL)
            return "Désolé, je n'ai pas trouvé de réponse dans ma base et l'IA externe n'a pas pu répondre."
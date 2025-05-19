from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from ia.loader import load_knowledge
from config import settings
from cluster.vram import memory
from colorama import Fore, Style
from groq import Groq
import torch, logging, time, PyPDF2, json, os

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
            logging.info("[INFO] Initialisation de HybridNLPEngine...")
            print(Fore.CYAN + "[INFO] Initialisation de HybridNLPEngine..." + Style.RESET_ALL)
            with open(settings.KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                self.cloud_knowledge = json.load(f)
            self.cloud_questions = [item["question"] for item in self.cloud_knowledge]
            self.cloud_answers = [item["reponse"] for item in self.cloud_knowledge]
            self.cloud_tfidf = TfidfVectorizer().fit(self.cloud_questions)
            self.cloud_vectors = self.cloud_tfidf.transform(self.cloud_questions)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors du chargement de la base de connaissances cloud : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors du chargement de la base de connaissances cloud : {e}" + Style.RESET_ALL)

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

    def find_best_pdf_passage(self, question, top_n=5, min_score=0.6):
        if not self.pdf_passages:
            return []
        vect = TfidfVectorizer().fit(self.pdf_passages + [question])
        tfidf = vect.transform(self.pdf_passages + [question])
        sims = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
        top_indices = sims.argsort()[-top_n:][::-1]
        return [(self.pdf_passages[i], sims[i]) for i in top_indices if sims[i] >= min_score]

    def ask_api(self, question, username=None, messages=None):
        try:
            if messages:
                prompt_messages = messages
            else:
                system_prompt = (
                    settings.PROMPT +
                    (f"\nL'utilisateur Discord avec qui tu échanges s'appelle : {username}. " if username else "") +
                    "Utilise ce prénom/pseudo dans tes réponses si c'est pertinent, mais ne le répète pas systématiquement. Sois naturel et pertinent."
                )
                prompt_messages = [{"role": "system", "content": system_prompt}]
                if question:
                    prompt_messages.append({"role": "user", "content": question})

            response = self.groq_client.chat.completions.create(
                model=settings.MODEL,
                messages=prompt_messages,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                top_p=settings.TOP_P,
                frequency_penalty=settings.FREQUENCY,
                presence_penalty=settings.PRESENCE_PENALTY,
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'appel à l'API IA : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'appel à l'API IA : {e}" + Style.RESET_ALL)
            return "Désolé, je n'ai pas trouvé de réponse dans ma base et l'IA externe n'a pas pu répondre."

    def get_answer(self, messages, username=None):
        try:
            # On récupère la dernière question posée par l'utilisateur
            question = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    question = msg["content"]
                    break
            if not question.strip():
                logging.warning("[WARNING] Question vide reçue.")
                return "Je ne peux pas répondre à une question vide."

            # Historique pour la mémoire utilisateur basée sur le pseudo uniquement
            if not hasattr(self, "user_histories"):
                self.user_histories = {}
            if username not in self.user_histories:
                self.user_histories[username] = []
            self.user_histories[username].append({"role": "user", "content": question})
            history = self.user_histories[username][-settings.LIMIT_MEMORY*2:]

            logging.info(f"[INFO] Question reçue : {question}")

            # Recherche TF-IDF
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

            # Recherche SBERT
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
            logging.warning("[WARNING] Aucune réponse pertinente trouvée. appel à l'IA")
            print(Fore.MAGENTA + "[INFO] Appel à ollama" + Style.RESET_ALL)
            #(((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))
            # Recherche dans cloud.json
            cloud_vector = self.cloud_tfidf.transform([question])
            cloud_similarity = cosine_similarity(cloud_vector, self.cloud_vectors)
            best_cloud_index = cloud_similarity.argmax()
            best_cloud_score = cloud_similarity[0, best_cloud_index]

            if best_cloud_score >= settings.MIN_SCORE_CLOUD:  # ajuste le seuil selon tes besoins
                logging.info(f"[INFO] Réponse trouvée dans cloud.json : {self.cloud_answers[best_cloud_index]}")
                return self.cloud_answers[best_cloud_index]

             # --- Amélioration du contexte PDF ---
            MAX_PASSAGE_LENGTH = settings.MAX_PASSAGE_LENGTH  # caractères max par passage
            TOP_N = settings.TOP_N # nombre de passages PDF à fournir
            pdf_passages = self.find_best_pdf_passage(question, top_n=TOP_N, min_score=settings.PDF_MIN_SCORE)
            pdf_passages = sorted(pdf_passages, key=lambda x: x[1], reverse=True)[:TOP_N]
            # Ajoute une instruction claire à l'IA

            if not messages or not isinstance(messages, list):
                messages = []
            messages.insert(0, {
                "role": "system",
                "content": (
                    "Utilise les extraits du PDF ci-dessous pour répondre à la question de l'utilisateur de façon précise et concise. "
                    "Si l'information n'est pas dans le PDF, indique-le clairement."
                )
            })

            for passage, score in pdf_passages:
                passage = passage[:MAX_PASSAGE_LENGTH] + "..." if len(passage) > MAX_PASSAGE_LENGTH else passage
                messages.append({
                    "role": "system",
                    "content": f"Extrait du PDF à utiliser pour répondre à la question suivante : '{question}'\n{passage}"
                })

            #(((((((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))))))
            api_response = self.ask_api(question, username, messages=messages)
            return api_response

        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la recherche de réponse : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la recherche de réponse : {e}" + Style.RESET_ALL)
            return "Désolé, une erreur s'est produite lors de la recherche de la réponse."


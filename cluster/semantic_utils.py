from sentence_transformers import SentenceTransformer, util
import json
import torch

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def charger_knowledge_embedding(filepath="knowledge.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    questions = [item["question"] for item in knowledge]
    embeddings = model.encode(questions, convert_to_tensor=True)

    return knowledge, embeddings

knowledge, knowledge_embeddings = charger_knowledge_embedding()

def chercher_reponse(question, seuil=0.6):
    question_embedding = model.encode(question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(question_embedding, knowledge_embeddings)[0]

    meilleur_score = torch.max(scores).item()
    meilleur_index = torch.argmax(scores).item()

    if meilleur_score < seuil:
        return "Désolé, je ne suis pas sûr de la réponse à ta question."

    return knowledge[meilleur_index]["answer"]

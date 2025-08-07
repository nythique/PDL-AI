import asyncio
import logging
import os
from typing import Dict, List, Optional, Union
import groq
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import threading
from datetime import datetime

class GroqMemoryManager: 
    def __init__(self):
        # Configuration des API Groq depuis les variables d'environnement
        self.api_configs = {
            "realtime": {
                "auth_token": os.getenv("GROQ_TOKEN_REALTIME"),
                "model": "mixtral-8x7b-32768",
                "timeout": 1.0,
                "max_tokens": 100
            },
            "sentiment": {
                "auth_token": os.getenv("GROQ_TOKEN_SENTIMENT"),
                "model": "mixtral-8x7b-32768",
                "timeout": 1.5,
                "max_tokens": 50
            },
            "background": {
                "auth_token": os.getenv("GROQ_TOKEN_BACKGROUND"),
                "model": "mixtral-8x7b-32768",
                "timeout": 3.0,
                "max_tokens": 500
            }
        }

        # Initialisation des clients Groq
        self.clients = {
            key: groq.Client(api_key=config["auth_token"])
            for key, config in self.api_configs.items()
        }

        # Cache pour les résultats
        self.cache = {
            "embeddings": {},
            "sentiment": {},
            "concepts": {}
        }

        # Verrous pour la gestion du cache
        self._cache_locks = {
            "embeddings": threading.Lock(),
            "sentiment": threading.Lock(),
            "concepts": threading.Lock()
        }

        # Pool d'exécution pour les appels API parallèles
        self.executor = ThreadPoolExecutor(max_workers=3)

    @lru_cache(maxsize=1000)
    async def get_semantic_embedding(self, content: str) -> dict:
        """Génère un embedding sémantique avec mise en cache."""
        cache_key = hash(content)

        with self._cache_locks["embeddings"]:
            if cache_key in self.cache["embeddings"]:
                return self.cache["embeddings"][cache_key]

        try:
            response = await self._call_groq_api(
                "realtime",
                prompt=f"Generate semantic embedding for: {content}",
                temperature=0.1
            )
            embedding = response["choices"][0]["text"]

            with self._cache_locks["embeddings"]:
                self.cache["embeddings"][cache_key] = embedding
                return embedding

        except Exception as e:
            logging.error(f"Erreur lors de la génération d'embedding: {e}")
            return None

    async def analyze_sentiment(self, content: str) -> float:
        """Analyse le sentiment avec l'API Groq."""
        cache_key = hash(content)

        with self._cache_locks["sentiment"]:
            if cache_key in self.cache["sentiment"]:
                return self.cache["sentiment"][cache_key]

        try:
            response = await self._call_groq_api(
                "sentiment",
                prompt=f"Analyze sentiment (return only a number between -1 and 1): {content}",
                temperature=0.1
            )
            sentiment = float(response["choices"][0]["text"])

            with self._cache_locks["sentiment"]:
                self.cache["sentiment"][cache_key] = sentiment
                return sentiment

        except Exception as e:
            logging.error(f"Erreur lors de l'analyse de sentiment: {e}")
            return 0.0

    async def extract_concepts(self, content: str) -> List[dict]:
        """Extrait les concepts avec l'API Groq."""
        cache_key = hash(content)

        with self._cache_locks["concepts"]:
            if cache_key in self.cache["concepts"]:
                return self.cache["concepts"][cache_key]

        try:
            response = await self._call_groq_api(
                "background",
                prompt=f"Extract key concepts and their importance (JSON format): {content}",
                temperature=0.1
            )
            concepts = eval(response["choices"][0]["text"])  # Attention: à sécuriser en production

            with self._cache_locks["concepts"]:
                self.cache["concepts"][cache_key] = concepts
                return concepts

        except Exception as e:
            logging.error(f"Erreur lors de l'extraction des concepts: {e}")
            return []

    async def _call_groq_api(self, api_type: str, prompt: str, temperature: float = 0.7) -> dict:
        """Appelle l'API Groq avec gestion des timeouts et erreurs."""
        client = self.clients[api_type]
        config = self.api_configs[api_type]

        try:
            async with asyncio.timeout(config["timeout"]):
                completion = await client.chat.completions.create(
                    model=config["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=config["max_tokens"],
                    temperature=temperature
                )
                return completion

        except asyncio.TimeoutError:
            logging.error(f"Timeout lors de l'appel à l'API Groq ({api_type})")
            raise
        except Exception as e:
            logging.error(f"Erreur lors de l'appel à l'API Groq ({api_type}): {e}")
            raise

    async def process_message(self, content: str) -> dict:
        """Traite un message avec tous les aspects d'analyse en parallèle."""
        tasks = [
            self.get_semantic_embedding(content),
            self.analyze_sentiment(content),
            self.extract_concepts(content)
        ]

        try:
            embedding, sentiment, concepts = await asyncio.gather(*tasks)
            return {
                "embedding": embedding,
                "sentiment": sentiment,
                "concepts": concepts,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Erreur lors du traitement du message: {e}")
            return None

    def clear_cache(self, cache_type: Optional[str] = None):
        """Nettoie le cache spécifié ou tous les caches."""
        if cache_type:
            with self._cache_locks[cache_type]:
                self.cache[cache_type].clear()
        else:
            for cache_type in self.cache:
                with self._cache_locks[cache_type]:
                    self.cache[cache_type].clear()

# Exemple d'utilisation
async def main():
    memory_manager = GroqMemoryManager()
    
    # Exemple de traitement d'un message
    message = "Je suis très content de cette nouvelle fonctionnalité !"
    result = await memory_manager.process_message(message)
    print(f"Résultat du traitement: {result}")

if __name__ == "__main__":
    asyncio.run(main())

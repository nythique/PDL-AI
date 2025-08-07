import datetime, os, json, logging, threading
from colorama import Fore, Style
from config import settings as statics

info_handler = logging.FileHandler(statics.SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(statics.ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)


class memory:
    def __init__(self, max_history=statics.ROM_LIMIT):
        try:
            logging.info("[INFO] Initialisation de la mémoire...")
            print(Fore.GREEN + "[INFO] Initialisation de la mémoire..." + Style.RESET_ALL)
            
            # Structure principale de données
            self.conversations = {}  # Messages par utilisateur
            self.channel_context = {}  # Contexte par canal
            self.semantic_memory = {}  # Mémoire sémantique pour éviter les répétitions
            self.interaction_patterns = {}  # Patterns d'interaction par utilisateur
            
            # Système d'apprentissage
            self.knowledge_base = {
                "concepts": {},          # Base de connaissances des concepts
                "patterns": {},          # Patterns de conversation appris
                "responses": {},         # Réponses efficaces
                "context_rules": {},     # Règles contextuelles apprises
                "user_preferences": {},  # Préférences apprises par utilisateur
            }
            
            # Métriques d'apprentissage
            self.learning_metrics = {
                "concept_frequency": {},      # Fréquence des concepts
                "pattern_success": {},        # Taux de succès des patterns
                "context_accuracy": 0.0,      # Précision de la détection de contexte
                "interaction_quality": {},    # Qualité des interactions par pattern
            }
            
            # Nouvelles structures pour imiter Grok
            self.conversation_threads = {}  # Suivi des fils de discussion
            self.topic_memory = {}  # Mémoire thématique
            self.user_preferences = {}  # Préférences et style de communication
            self.global_context = []  # Contexte global pour l'apprentissage
            
            # Paramètres de configuration
            self.max_history = max_history
            self.channel_context_limit = 50
            self.semantic_threshold = 0.85  # Seuil de similarité sémantique
            self.context_depth = 3  # Niveaux de contexte à maintenir
            self.last_message_time = {}
            self.modified = False
            self._lock = threading.RLock()
            self.load_from_file()
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de l'initialisation de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation de la mémoire" + Style.RESET_ALL)
            raise  # Propager l'erreur pour une meilleure gestion

    def clear_context(self, inactive_time_threshold=statics.MEMORY_MAX_INACTIVE_TIME * 3600):
        """Supprime la mémoire des utilisateurs inactifs depuis plus de inactive_time_threshold secondes."""
        try:
            logging.info("[INFO] Suppression de la mémoire des utilisateurs inactifs...")
            print(Fore.GREEN + "[INFO] Suppression de la mémoire des utilisateurs inactifs..." + Style.RESET_ALL)
            now = datetime.datetime.now()
            to_remove = []
            for user_id, last_time in self.last_message_time.items():
                if (now - last_time).total_seconds() > inactive_time_threshold:
                    to_remove.append(user_id)
            for user_id in to_remove:
                self.conversations.pop(user_id, None)
                self.last_message_time.pop(user_id, None)
                self.modified = True
                logging.info(f"[INFO] Mémoire supprimée pour l'utilisateur {user_id}.")
                print(Fore.YELLOW + f"[INFO] Mémoire supprimée pour l'utilisateur {user_id}." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la suppression de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la suppression de la mémoire" + Style.RESET_ALL)

    def manage(self, user_id, message_content, channel_id=None, is_bot_message=False, mentions=None):
        """Gère la mémoire des utilisateurs avec apprentissage dynamique et contexte enrichi."""
        try:
            logging.info("[INFO] Gestion de la mémoire...")
            print(Fore.GREEN + "[INFO] Gestion de la mémoire..." + Style.RESET_ALL)
            
            with self._lock:
                user_id = str(user_id)
                channel_id = str(channel_id) if channel_id else None
                current_time = datetime.datetime.now()
                
                # Structure de message enrichie
                message_data = {
                    "content": message_content,
                    "timestamp": current_time.isoformat(),
                    "is_bot": is_bot_message,
                    "mentions": mentions or [],
                    "semantic_embedding": self._generate_semantic_key(message_content)
                }
                
                # Gestion du contexte de canal
                if channel_id:
                    if channel_id not in self.channel_context:
                        self.channel_context[channel_id] = []
                    
                    self.channel_context[channel_id].append({
                        "user_id": user_id,
                        **message_data
                    })
                    
                    # Limiter le contexte de canal
                    if len(self.channel_context[channel_id]) > self.channel_context_limit:
                        self.channel_context[channel_id] = self.channel_context[channel_id][-self.channel_context_limit:]
                
                # Gestion de la conversation utilisateur
                if user_id not in self.conversations:
                    self.conversations[user_id] = []
                    self.semantic_memory[user_id] = set()
                    self.interaction_patterns[user_id] = {
                        "frequent_topics": {},
                        "response_style": {},
                        "interaction_time": []
                    }
                
                # Vérification de la répétition sémantique
                semantic_key = message_data["semantic_embedding"]
                if semantic_key not in self.semantic_memory[user_id]:
                    self.conversations[user_id].append(message_data)
                    self.semantic_memory[user_id].add(semantic_key)
                    self.modified = True
                    
                    # Mise à jour des patterns d'interaction
                    self._update_interaction_patterns(user_id, message_data)
                    
                    # Mettre à jour le timestamp
                    self.last_message_time[user_id] = current_time
                    
                    # Limiter l'historique tout en préservant le contexte important
                    if self.max_history > 0:
                        self.conversations[user_id] = self._smart_trim_history(user_id)
                    
                    # Sauvegarde périodique
                    if len(self.conversations[user_id]) % 5 == 0:
                        self.save_to_file()
            logging.info(f"[INFO] Mémoire mise à jour pour l'utilisateur {user_id}.")
            print(Fore.YELLOW + f"[INFO] Mémoire mise à jour pour l'utilisateur {user_id}." + Style.RESET_ALL)
            return self.conversations[user_id]
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la gestion de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la gestion de la mémoire" + Style.RESET_ALL)

    def get_history(self, user_id):
        """Récupère l'historique des messages d'un utilisateur."""
        try:
            logging.info("[INFO] Récupération de l'historique...")
            with self._lock:  # Protection des accès concurrents
                user_id = str(user_id)
                history = self.conversations.get(user_id, []).copy()  # Copie pour éviter les modifications concurrentes
                return history
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la récupération de l'historique : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la récupération de l'historique" + Style.RESET_ALL)
            raise  # Propager l'erreur pour une meilleure gestion

    def save_to_file(self):
        """Sauvegarde la mémoire dans un fichier de manière atomique."""
        try:
            with self._lock:  # Protection des accès concurrents
                if not self.modified:  # Éviter les sauvegardes inutiles
                    return
                    
                logging.info("[INFO] Sauvegarde de la mémoire...")
                print(Fore.GREEN + "[INFO] Sauvegarde de la mémoire..." + Style.RESET_ALL)
                
                # Création d'un fichier temporaire pour la sauvegarde atomique
                temp_file = f"{statics.ROM_PATH}.tmp"
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "conversations": self.conversations,
                        "last_message_time": {k: v.isoformat() for k, v in self.last_message_time.items()}
                    }, f, indent=4, ensure_ascii=False)
                
                # Remplacement atomique du fichier
                os.replace(temp_file, statics.ROM_PATH)
                self.modified = False
                
                logging.info("[INFO] Mémoire sauvegardée avec succès.")
                print(Fore.YELLOW + "[INFO] Mémoire sauvegardée avec succès." + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la sauvegarde de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la sauvegarde de la mémoire" + Style.RESET_ALL)
            if 'temp_file' in locals() and os.path.exists(temp_file):
                os.remove(temp_file)  # Nettoyage en cas d'erreur
            raise

    def _generate_semantic_key(self, content):
        """Génère une empreinte sémantique avancée du contenu."""
        try:
            # Prétraitement
            content = content.lower()
            words = content.split()
            
            # Extraction de concepts clés
            concepts = self._extract_concepts(words)
            
            # Analyse des relations
            relations = self._analyze_semantic_relations(concepts)
            
            # Génération d'une empreinte unique
            semantic_fingerprint = {
                "concepts": concepts,
                "relations": relations,
                "sentiment": self._analyze_sentiment(content),
                "context_type": self._determine_context_type(content),
                "topic_vectors": self._generate_topic_vectors(content)
            }
            
            # Création d'une clé unique basée sur l'ensemble des caractéristiques
            return hash(str(sorted(semantic_fingerprint.items())))
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse sémantique: {e}")
            return hash(content)  # Fallback sur la méthode simple
            
    def _extract_concepts(self, words):
        """Extrait les concepts clés du texte."""
        concepts = {}
        current_phrase = []
        
        for word in words:
            current_phrase.append(word)
            if len(current_phrase) > 3:
                phrase = " ".join(current_phrase[-3:])
                if self._is_meaningful_concept(phrase):
                    concepts[phrase] = self._calculate_concept_weight(phrase)
        
        return concepts
        
    def _is_meaningful_concept(self, phrase):
        """Détermine si une phrase représente un concept significatif."""
        # Filtres de pertinence
        stop_words = {"le", "la", "les", "un", "une", "des", "et", "ou", "mais"}
        words = phrase.split()
        
        return (
            len(words) > 1 and  # Multi-mots uniquement
            not all(w in stop_words for w in words) and  # Pas que des stop words
            any(len(w) > 3 for w in words)  # Au moins un mot significatif
        )
        
    def _calculate_concept_weight(self, concept):
        """Calcule le poids d'un concept basé sur sa pertinence."""
        weight = 1.0
        
        # Bonus pour les concepts techniques ou spécifiques
        if any(indicator in concept.lower() for indicator in [
            "fonction", "méthode", "classe", "api", "système",
            "error", "bug", "problème", "solution"
        ]):
            weight *= 1.5
            
        # Bonus pour les concepts déjà présents dans d'autres conversations
        if self._concept_exists_in_history(concept):
            weight *= 1.3
            
        return weight
    
    def _update_interaction_patterns(self, user_id, message_data):
        """Met à jour les patterns d'interaction de l'utilisateur."""
        patterns = self.interaction_patterns[user_id]
        content = message_data["content"].lower()
        
        # Analyse des sujets fréquents
        words = content.split()
        for word in words:
            if len(word) > 3:  # Ignorer les mots très courts
                patterns["frequent_topics"][word] = patterns["frequent_topics"].get(word, 0) + 1
        
        # Enregistrer l'heure d'interaction
        hour = datetime.datetime.fromisoformat(message_data["timestamp"]).hour
        patterns["interaction_time"].append(hour)
        if len(patterns["interaction_time"]) > 100:
            patterns["interaction_time"] = patterns["interaction_time"][-100:]
    
    def _smart_trim_history(self, user_id):
        """Effectue un élagage intelligent de l'historique en préservant les messages importants."""
        messages = self.conversations[user_id]
        if len(messages) <= self.max_history:
            return messages
            
        # Garder les messages récents
        recent_messages = messages[-int(self.max_history * 0.6):]
        
        # Sélectionner des messages importants du passé
        old_messages = messages[:-int(self.max_history * 0.6)]
        important_old = []
        
        for msg in old_messages:
            # Critères d'importance : mentions, longueur, etc.
            if len(msg["content"]) > 100 or msg["mentions"] or self._is_conceptually_important(msg):
                important_old.append(msg)
        
        # Combiner en préservant l'ordre chronologique
        return important_old[-int(self.max_history * 0.4):] + recent_messages
    
    def _is_conceptually_important(self, message):
        """Détermine si un message est conceptuellement important."""
        content = message["content"].lower()
        
        # Mots clés indiquant l'importance
        important_indicators = {
            "définition", "exemple", "important", "attention", "noter",
            "rappel", "conclusion", "résumé", "explique", "comprendre"
        }
        
        # Vérifier les indicateurs d'importance
        return any(indicator in content for indicator in important_indicators)
    
    def get_channel_context(self, channel_id, limit=10):
        """Récupère le contexte récent d'un canal."""
        with self._lock:
            channel_id = str(channel_id)
            if channel_id in self.channel_context:
                return self.channel_context[channel_id][-limit:]
            return []
    
    def get_interaction_insights(self, user_id):
        """Récupère des insights sur les interactions de l'utilisateur."""
        with self._lock:
            user_id = str(user_id)
            if user_id in self.interaction_patterns:
                patterns = self.interaction_patterns[user_id]
                return {
                    "frequent_topics": dict(sorted(patterns["frequent_topics"].items(), 
                                                 key=lambda x: x[1], 
                                                 reverse=True)[:10]),
                    "active_hours": self._analyze_active_hours(patterns["interaction_time"]),
                }
            return None
    
    def _analyze_semantic_relations(self, concepts):
        """Analyse les relations sémantiques entre concepts."""
        relations = {}
        
        for concept1 in concepts:
            for concept2 in concepts:
                if concept1 != concept2:
                    relation_strength = self._calculate_relation_strength(concept1, concept2)
                    if relation_strength > 0.5:  # Seuil minimal de relation
                        relations[f"{concept1}|{concept2}"] = relation_strength
        
        return relations

    def _calculate_relation_strength(self, concept1, concept2):
        """Calcule la force de la relation entre deux concepts."""
        # Vérification dans l'historique global
        cooccurrence = self._get_concept_cooccurrence(concept1, concept2)
        temporal_proximity = self._get_temporal_proximity(concept1, concept2)
        semantic_similarity = self._get_semantic_similarity(concept1, concept2)
        
        # Moyenne pondérée des facteurs
        return (cooccurrence * 0.4 + temporal_proximity * 0.3 + semantic_similarity * 0.3)

    def _analyze_sentiment(self, content):
        """Analyse le sentiment du message."""
        # Dictionnaire simple de mots positifs/négatifs
        positive_words = {"bien", "super", "excellent", "merci", "parfait", "génial"}
        negative_words = {"problème", "erreur", "bug", "mauvais", "difficile"}
        
        words = content.lower().split()
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return 0  # Neutre
        return (positive_count - negative_count) / total

    def _determine_context_type(self, content):
        """Détermine le type de contexte du message."""
        context_indicators = {
            "question": {"?", "comment", "pourquoi", "quand", "où", "qui", "que"},
            "information": {"voici", "voilà", "c'est", "il y a", "donc"},
            "action": {"faire", "créer", "modifier", "supprimer", "ajouter"},
            "feedback": {"merci", "d'accord", "ok", "compris", "je vois"}
        }
        
        content_lower = content.lower()
        context_scores = {}
        
        for context_type, indicators in context_indicators.items():
            score = sum(1 for ind in indicators if ind in content_lower)
            context_scores[context_type] = score
            
        return max(context_scores.items(), key=lambda x: x[1])[0]

    def _generate_topic_vectors(self, content):
        """Génère des vecteurs de sujets pour le contenu."""
        topics = {
            "technique": {"code", "fonction", "erreur", "fichier", "système"},
            "support": {"aide", "problème", "besoin", "question"},
            "feedback": {"merci", "super", "bien", "mal"},
            "action": {"faire", "créer", "modifier", "changer"}
        }
        
        content_words = set(content.lower().split())
        return {
            topic: len(words & content_words) / len(words)
            for topic, words in topics.items()
        }

    def _learn_from_interaction(self, user_id, message_data, response_data=None):
        """Apprentissage à partir d'une interaction."""
        try:
            # 1. Extraction des patterns
            patterns = self._extract_interaction_patterns(message_data)
            
            # 2. Mise à jour de la base de connaissances
            self._update_knowledge_base(patterns, response_data)
            
            # 3. Ajustement des poids d'apprentissage
            self._adjust_learning_weights(user_id, patterns)
            
            # 4. Évaluation et optimisation
            self._evaluate_learning_performance()
            
        except Exception as e:
            logging.error(f"Erreur lors de l'apprentissage : {e}")
            
    def _extract_interaction_patterns(self, message_data):
        """Extrait les patterns d'une interaction."""
        patterns = {
            "linguistic": self._analyze_linguistic_patterns(message_data["content"]),
            "temporal": self._analyze_temporal_patterns(message_data["timestamp"]),
            "contextual": self._analyze_contextual_patterns(message_data),
            "semantic": self._analyze_semantic_patterns(message_data["content"])
        }
        return patterns
        
    def _update_knowledge_base(self, patterns, response_data):
        """Met à jour la base de connaissances avec les nouveaux patterns."""
        for pattern_type, pattern_data in patterns.items():
            if pattern_type not in self.knowledge_base["patterns"]:
                self.knowledge_base["patterns"][pattern_type] = {}
                
            # Mise à jour avec pondération temporelle
            current_weight = 0.7  # Les nouveaux patterns ont plus de poids
            for pattern, score in pattern_data.items():
                existing_score = self.knowledge_base["patterns"][pattern_type].get(pattern, 0)
                new_score = (existing_score * (1 - current_weight) + score * current_weight)
                self.knowledge_base["patterns"][pattern_type][pattern] = new_score
                
    def _adjust_learning_weights(self, user_id, patterns):
        """Ajuste les poids d'apprentissage basés sur le succès des interactions."""
        if user_id not in self.learning_metrics["interaction_quality"]:
            self.learning_metrics["interaction_quality"][user_id] = 0.5
            
        # Calcul du score de qualité
        pattern_success = self._calculate_pattern_success(patterns)
        
        # Mise à jour de la qualité d'interaction
        current_quality = self.learning_metrics["interaction_quality"][user_id]
        self.learning_metrics["interaction_quality"][user_id] = (
            current_quality * 0.8 + pattern_success * 0.2
        )
        
    def _calculate_pattern_success(self, patterns):
        """Calcule le taux de succès des patterns."""
        success_scores = []
        
        for pattern_type, pattern_data in patterns.items():
            if pattern_type in self.knowledge_base["patterns"]:
                known_patterns = self.knowledge_base["patterns"][pattern_type]
                
                # Compare les nouveaux patterns avec les patterns connus
                for pattern, score in pattern_data.items():
                    if pattern in known_patterns:
                        similarity = abs(known_patterns[pattern] - score)
                        success_scores.append(1.0 - similarity)
                        
        return sum(success_scores) / len(success_scores) if success_scores else 0.5
        
    def _evaluate_learning_performance(self):
        """Évalue et optimise la performance d'apprentissage."""
        # Calcul de la précision globale
        accuracy = sum(self.learning_metrics["interaction_quality"].values()) / len(
            self.learning_metrics["interaction_quality"]
        ) if self.learning_metrics["interaction_quality"] else 0
        
        self.learning_metrics["context_accuracy"] = accuracy
        
        # Optimisation basée sur la performance
        if accuracy < 0.5:
            # Augmenter la sensibilité d'apprentissage
            self.semantic_threshold *= 0.95
        elif accuracy > 0.8:
            # Réduire la sensibilité pour éviter le surapprentissage
            self.semantic_threshold = min(0.95, self.semantic_threshold * 1.05)

    def _analyze_active_hours(self, timestamps):
        """Analyse les heures actives de l'utilisateur."""
        if not timestamps:
            return []
        
        hour_counts = [0] * 24
        for hour in timestamps:
            hour_counts[hour] += 1
            
        # Retourner les heures les plus actives
        active_hours = []
        for hour, count in enumerate(hour_counts):
            if count > len(timestamps) * 0.1:  # Plus de 10% des interactions
                active_hours.append(hour)
        return active_hours

    def load_from_file(self):
        """Charge la mémoire depuis un fichier JSON."""
        try:
            logging.info("[INFO] Vérification du fichier de mémoire...")
            if not os.path.exists(statics.ROM_PATH):
                return
            logging.info("[INFO] Fichier de mémoire verifié.")
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors de la vérification du fichier de mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors de la vérification du fichier de mémoire" + Style.RESET_ALL)
            return
        try:
            logging.info("[INFO] Chargement de la mémoire...")
            with open(statics.ROM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.conversations = data.get("conversations", {})
                self.last_message_time = {
                    k: datetime.datetime.fromisoformat(v) for k, v in data.get("last_message_time", {}).items()
                }
            logging.info("[INFO] Mémoire chargée avec succès.")
        except Exception as e:
            logging.error(f"[ERROR] Erreur lors du chargement de la mémoire : {e}")
            print(Fore.RED + f"[ERROR] Erreur lors du chargement de la mémoire" + Style.RESET_ALL)
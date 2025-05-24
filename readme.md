# DiscordBot IA (base locale + PDF)

Un bot Discord doté d'une IA hybride : il répond aux questions à partir d'une base de connaissances locale (TF-IDF/SBERT), peut apprendre de nouvelles réponses, et exploite aussi des documents PDF comme source d'information pour l'IA générative (LLM).  
Le bot gère la mémoire utilisateur, l'analyse d'images (OCR), la journalisation avancée, et propose des commandes d'administration.

---

## Fonctionnalités principales

- **Fallback IA générative** (Groq/Ollama) avec enrichissement 
- **OCR** : extraction de texte depuis des images
- **Journalisation** complète des événements et erreurs
- **Gestion de la mémoire** (contexte utilisateur, historique)
- **Commandes d'administration** (vider logs, redémarrer, etc.)

---

## Installation

1. **Installer les dépendances Python :**
    ```bash
    pip install -r upload.txt
    ```

2. **Installer Tesseract OCR :**
    - **Windows** : [Télécharger ici](https://github.com/tesseract-ocr/tesseract/releases)
    - **Linux/Mac** :  
      ```bash
      sudo apt install tesseract-ocr
      ```

3. **Configurer le bot :**
    - Remplir les paramètres dans `config/settings.py` (token, clés API, chemins, etc.)

4. **Lancer le bot :**
    ```bash
    python starter.py
    ```
    ou utiliser `start.bat` (recommandé sur VM/Windows)

---

## Notes

- **Logs** : consultables dans `logs/`
- **OCR** : fonctionne sur images envoyées en DM ou sur le serveur


**Développé par Nythique • PDL IA**
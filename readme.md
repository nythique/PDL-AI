# DiscordBot IA (base locale + PDF)

Un bot Discord doté d'une IA hybride : il répond aux questions à partir d'une base de connaissances locale (TF-IDF/SBERT), peut apprendre de nouvelles réponses, et exploite aussi des documents PDF comme source d'information pour l'IA générative (LLM).  
Le bot gère la mémoire utilisateur, l'analyse d'images (OCR), la journalisation avancée, et propose des commandes d'administration.

---

## Fonctionnalités principales

- **Réponses automatiques** via base de connaissances locale (TF-IDF/SBERT)
- **Fallback IA générative** (Groq/Ollama) avec enrichissement par extraits PDF
- **Ajout de connaissances** par commande Discord
- **Analyse de PDF** pour fournir des réponses précises
- **OCR** : extraction de texte depuis des images
- **Journalisation** complète des événements et erreurs
- **Gestion de la mémoire** (contexte utilisateur, historique)
- **Commandes d'administration** (vider logs, redémarrer, etc.)

---

## Installation

1. **Installer les dépendances Python :**
    ```bash
    pip install -r requirements.txt
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
    python main.py
    ```
    ou utiliser `start.bat` (recommandé sur VM/Windows)

---

## Exemple d’utilisation

- **Question simple :**  
  « Quels sont les bienfaits du curcuma ? »
- **Question sur le PDF :**  
  « Que dit le document sur la sécurité alimentaire ? »
- **Ajout de connaissance :**  
  `/commit <question> <réponse>`

---

## Structure du projet

```
DiscordBot IA/
│
├── main.py                    # Point d'entrée du programme
├── bot.py                     # Lanceur du bot
├── start.bat                  # Script de démarrage (Windows)
│
├── cluster/
│   ├── vram.py                # Gestion mémoire utilisateur
│   └── chat/
│       └── thread.json        # Mémoire persistente pour TF-IDF/SBERT
│
├── config/
│   └── settings.py            # Configuration globale
│
├── core/
│   ├── client.py              # Configuration du bot Discord
│   ├── commands.py            # Commandes et événements Discord
│   └── validation.py          # Validation des ajouts
│
├── ia/
│   ├── loader.py              # Chargement de la base JSON
│   ├── nlp.py                 # Traitement texte (TF-IDF, SBERT, LLM, PDF)
│   └── server/                # Fichiers nécessaires (JSON, PDF)
│
├── logs/
│   └── bot.log                # Fichier de logs généré automatiquement
│
├── tools/
│   ├── temp/                  # Images temporaires téléchargées
│   ├── cleaner.py             # Filtrage/validation des ajouts
│   └── ocr.py                 # Analyse d'image (OCR)
│
├── requirements.txt           # Modules requis
└── README.md                  # Documentation
```

---

## Notes

- **Base de connaissances** : modifiable dans `ia/knowledge.json`
- **PDF** : placez vos documents dans `ia/server/`
- **Logs** : consultables dans `logs/bot.log`
- **OCR** : fonctionne sur images envoyées en DM ou sur le serveur

---

**Développé par Nythique • PDL IA**
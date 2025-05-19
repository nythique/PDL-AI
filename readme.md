# DiscordBot IA (local database)

Un bot Discord avec une IA simple basée sur TF-IDF pour répondre à des questions selon une base de connaissances locale, disposant d'une capacité d'apprentissage et d'analyse pour un developpement constant  de sa base de donnée locale.
Une journalisation des different evenement du bot est incluse dans le système.

## Structure

- `main.py` : point d'entrée du programme.
- `bot.py` : instancie le bot et connecte les événements.
- `cluster/` : gestion de la memoire.
- `core/` : logique Discord (client et événements).
- `ia/` : moteur IA + base de connaissances.
- `logs/` : Journalisation.
- `tools/` : fonctionnalitées additionnelles.
- `config/settings.py` : configuration centrale.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```
Installez également Tesseract OCR sur votre système:
   Windows : Téléchargez et installez Tesseract OCR(https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe).
   Linux/Mac : Utilisez votre gestionnaire de paquets, par exemple :
```
sudo apt install tesseract-ocr
```

2. Remplacer le token (et la configuration de base) dans `config/settings.py`.

3. Lancer le bot :
```bash
python main.py Où start start.bat (récommande vm)
```

## Exemple de question

- "Quels sont les bienfaits du curcuma ?"
- "Comment utiliser le gingembre ?"

**Notes:** Tu peux ajouter d'autres questions/réponses (respecter la syntax) dans `ia/knowledge.json`.

## Plan detaillé 

```
DiscordBot IA/
│
├── bot.py                     # Lanceur du bot (point d’entrée)
├── main.py                    # Pour exécuter par start.bat
├── start.bat                  # Fichier pour executer primcipal
│
├── cluster/
│   └── vram.py                # Gestionnaire de la memoire partielle
│   └── chat/
│       └── thread.json        # Memoire persistente pour IDF et SERB
│             
├── config/
│   └── settings.py            # Config globale
│
├── core/
│   ├── client.py              # Classe pour configurer le bot Discord
│   └── commands.py            # Commandes/événements Discord
│   └── validation.py          # Commandes de push
├── ia/
│   ├── loader.py              # Lecture de la base JSON
│   ├── nlp.py                 # Traitement de texte (TF-IDF, SERB, llama) 
│   └── server /
│       └── (Ensemble des fichier requis (deux json et un pdf))
│
├── logs/
│   └── bot.log               # Fichier de logs généré automatiquement
│
├── tools/
│   └── temp /  (Dossier pour les image temporaire telecharger)
│   └── cleaner.py           # Outil de filtrage pour les ajout en memoire
│   └── ocr.py               # Fichier d'analyse d'image
│
├── requirements.txt         # Module requis
└── README.md                # Documentation
```



# Mon Bot IA (Discord)

Un bot Discord avec une IA simple basée sur TF-IDF pour répondre à des questions selon une base de connaissances locale, disposant d'une capacité d'apprentissage et d'analyse pour un developpement constant  de sa base de donnée locale.
Une journalisation des different evenement du bot est incluse dans le système.

## Structure

- `main.py` : point d'entrée du programme.
- `bot.py` : instancie le bot et connecte les événements.
- `core/` : logique Discord (client et événements).
- `ia/` : moteur IA + base de connaissances.
- `config/settings.py` : configuration centrale.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Remplacer le token (et la configuration de base) dans `config/settings.py`.

3. Lancer le bot :
```bash
python main.py
```

## Exemple de question

- "Quels sont les bienfaits du curcuma ?"
- "Comment utiliser le gingembre ?"

**Notes:** Tu peux ajouter d'autres questions/réponses (respecter la syntax) dans `ia/knowledge.json`.

## Plan detaillé 

```
DiscordBot IA/
│
├── bot.py                      # Lanceur du bot (point d’entrée)
├── main.py                     # Pour exécuter tout proprement
│
├── config/
│   └── settings.py             # Config globale (token, chemins, seuils, etc.)
│
├── core/
│   ├── client.py           # Classe pour configurer le bot Discord
│   └── commands.py             # Commandes/événements Discord
│
├── ia/
│   ├── loader.py          # Lecture de la base JSON ou autre
│   ├── nlp.py           # Traitement de texte (TF-IDF, recherche) - C’est le cerveau du bot
│   └── captured_qr.json          # Données de Q/R apprise automatiquement (à valider avec /push)
│   └── knowledge.json          # Tes données de questions/réponses
│
├── logs/
│   └── bot.log                 # Fichier de logs généré automatiquement
│
├── requirements.txt             # Module requis
└── README.md                # Documentation
```

### Résumé visuel du flux :
```
main.py
   └── bot.py
         ├── client.py => crée le bot
         └── validation.py => Validation des Q/R detecter par le bot
         └── commands.py   => lie les événements et commandes du bot
                  └── nlp.py => traite les questions
                          └── loader.py => lit le fichier JSON
```


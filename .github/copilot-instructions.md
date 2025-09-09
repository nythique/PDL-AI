# Instructions pour les agents AI - PDL-AI Bot

## Architecture et Structure du Projet

Ce projet est un bot Discord développé en Python avec une architecture modulaire. Voici les composants principaux :

### Structure des Dossiers
- `/bot` - Point d'entrée et configuration principale
- `/commands` - Commandes du bot (admin et public)
- `/config` - Paramètres de configuration
- `/home` - Logique métier principale
- `/plugins` - Plugins et intégrations externes
- `/logs` - Journaux d'erreurs et de sécurité

### Composants Clés

1. **Système de Bot Principal** (`bot/bot.py`)
   - Utilise discord.py avec des extensions (cogs)
   - Système de logging centralisé pour la sécurité et les erreurs
   - Chargement dynamique des cogs au démarrage

2. **Gestion de la Configuration** (`config/settings.py`)
   - Centralise les constantes et paramètres
   - Définit les chemins des logs et autres configurations

3. **Système de Stockage** (`plugins/integrating/storing/database.py`)
   - Gestion de la mémoire avec système de verrou (RLock)
   - Structure de données JSON pour la persistance
   - Clés principales : Root Users, Bot Status, Allowed Channels, Bot Stats

## Conventions de Code

### Logging
```python
logging.info("[INFO] Message d'information")
logging.error("[ERROR] Message d'erreur", exc_info=True)
```

### Gestion des Erreurs
- Utiliser des blocs try/except avec logging détaillé
- Toujours inclure exc_info=True pour les erreurs
- Logger dans les fichiers appropriés (ERROR_LOG_PATH, SECURITY_LOG_PATH)

## Workflows de Développement

### Installation
```shell
# Installation des dépendances
poetry install

# Configuration de l'environnement
cp config/settings.example.py config/settings.py
# Éditer settings.py avec vos paramètres
```

### Tests et Débogage
- Les logs sont stockés dans `/logs/error/` et `/logs/security/`
- Utiliser les commandes de débogage admin (`commands.admin.debug`)

## Intégrations Externes

- **Lavalink** (`plugins/integrating/hosting/node_lavalink.py`) - Pour la gestion audio
- **Base de données** (`plugins/integrating/storing/database.py`) - Stockage persistant
- **Reconnaissance** (`plugins/processing/recognition/`) - OCR et reconnaissance vocale

## Points d'Attention Particuliers

1. **Gestion de la Mémoire**
   - Utiliser les verrous (RLock) lors de l'accès aux données partagées
   - Suivre le modèle de la classe Database pour la persistance

2. **Sécurité**
   - Vérifier les permissions avec le système de Root Users
   - Logger toutes les actions sensibles dans security.log

3. **Performance**
   - Utiliser asyncio pour les opérations asynchrones
   - Éviter les opérations bloquantes dans la boucle principale

## Exemples de Code

### Ajout d'une Nouvelle Commande
```python
@commands.command()
async def nouvelle_commande(self, ctx):
    try:
        logging.info("[INFO] Exécution de nouvelle_commande")
        # Votre code ici
    except Exception as e:
        logging.error("[ERROR] Erreur dans nouvelle_commande", exc_info=True)
```

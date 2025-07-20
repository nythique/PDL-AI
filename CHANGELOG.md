# Changelog

## [2.0.0] - 2025-07-19

### Ajouté
- Système de migration de données avec sauvegarde automatique
- Logs rotatifs (1MB max, 5 backups)
- Verrous pour la gestion concurrente des données
- Documentation détaillée du code
- Validation des types de données
- Sauvegarde atomique avec fichier temporaire

### Modifié
- Structure du classement utilisateur
  - Ajout du timestamp de dernière mise à jour
  - Support des achievements
- Nouvelles statistiques du bot
  - Temps passé en vocal
  - Commandes par jour
- Utilisation de constantes pour les clés de la base de données

### Sécurité
- Protection contre la corruption des données
- Validation des entrées utilisateur
- Gestion améliorée des erreurs
- Sauvegarde automatique avant migration

### Technique
- Refactoring complet de la classe Database
- Optimisation des accès concurrents
- Meilleure gestion des logs
- Support du versioning de la base de données

## [1.0.0] - Version initiale

### Fonctionnalités
- Gestion des utilisateurs root
- Système de classement simple
- Statistiques de base du bot
- Gestion des canaux autorisés
- Système de sauvegarde basique

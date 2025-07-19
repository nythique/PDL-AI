# Politique de sécurité

La sécurité de ce projet est une priorité. Merci de contribuer à la protection de l’écosystème et des utilisateurs.

## Vulnérabilités potentielles

- Fuite ou compromission du token Discord / API key (réinitialisé automatiquement si détecté par Github)
- Commandes sensibles sans contrôle d’accès strict
- Injection de code ou de commandes via les entrées utilisateur
- Exposition de données sensibles (logs, fichiers de configuration, etc.)
- Utilisation de dépendances non sécurisées
- Gestion inadéquate des fichiers ou des permissions
- Absence de limitation sur les actions utilisateur (risque de spam ou de déni de service)

## Bonnes pratiques recommandées

- Stocker les secrets (tokens, clés API) dans des variables d’environnement
- Implémenter des contrôles d’accès pour toutes les commandes critiques
- Valider et filtrer systématiquement toutes les entrées utilisateur
- Maintenir les dépendances à jour et surveiller les alertes de sécurité
- Limiter la quantité d’informations sensibles dans les logs
- Appliquer des limites de fréquence (rate limiting) sur les actions utilisateur

## Procédure de signalement

Si vous identifiez une faille de sécurité :

1. **Ne la divulguez pas publiquement.**
2. Contactez le mainteneur du projet en privé :
   - Email : [votre.email@domaine.com]
3. Fournissez un maximum de détails pour permettre la reproduction et la correction du problème.

Nous nous engageons à traiter tout signalement dans les meilleurs délais.

Merci pour votre vigilance et votre professionnalisme. 
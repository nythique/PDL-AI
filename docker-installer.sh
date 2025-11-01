#!/bin/bash
#==================================================================
# docker-installer.sh - Script to install Docker on Fedora
# This script is intended for Fedora systems and requires sudo privileges.
# Usage: ./docker-installer.sh
# Author: nythique (adapté pour Fedora)
# License: GNU AFFERO GENERAL PUBLIC LICENSE
# Version: 1.1
# Date: 2025-11-01
#==================================================================

set -euo pipefail

echo "==================🚀 Vérification de l'OS...=================="
if [ -f /etc/os-release ]; then
    . /etc/os-release
else
    echo "Impossible de détecter le système (fichier /etc/os-release manquant)." >&2
    exit 1
fi

if [ "${ID:-}" != "fedora" ]; then
    echo "Avertissement : ce script est conçu pour Fedora. OS détecté : ${ID:-unknown}." >&2
    read -r -p "Voulez-vous continuer quand même ? (y/N) " answer
    if [[ "${answer,,}" != "y" ]]; then
        echo "Annulation."; exit 1
    fi
fi

echo "==================🔄 Mise à jour du système...=================="
sudo dnf -y upgrade --refresh

echo "📦 Installation des dépendances requises..."
sudo dnf install -y dnf-plugins-core ca-certificates curl gnupg
clear

echo "==================📦 Ajout du dépôt officiel Docker pour Fedora...=================="
# Le dépôt officiel fournit les paquets Docker pour Fedora
echo "Tentative d'ajout du dépôt via dnf config-manager..."
if sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo 2>/dev/null; then
    echo "Dépôt ajouté via config-manager."
else
    echo "config-manager ne supporte pas --add-repo ou a échoué, ajout manuel du fichier de repo..."
    if sudo curl -fsSL https://download.docker.com/linux/fedora/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo; then
        echo "Fichier de repo écrit dans /etc/yum.repos.d/docker-ce.repo"
    else
        echo "Erreur : impossible d'écrire /etc/yum.repos.d/docker-ce.repo" >&2
        exit 1
    fi
fi
clear

echo "==================🔄 Mise à jour du cache des paquets...=================="
sudo dnf makecache
clear

echo "==================🐳 Installation de Docker Engine et plugins...=================="
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
clear

echo "==================🔛 Activation et démarrage du service Docker...=================="
sudo systemctl enable --now docker
sudo systemctl status --no-pager --full docker || true
clear

echo "==================👤 Ajout de l'utilisateur ${USER} au groupe docker...=================="
sudo usermod -aG docker "$USER"
clear

echo "==================✅ Installation terminée" 
echo "Pour tester Docker maintenant :"
echo "  1) Rechargez votre session (déconnexion/connexion) ou exécutez : newgrp docker"
echo "  2) Lancez : docker run hello-world"
echo "Si vous n'avez pas de session graphique, exécutez : exec su -l $USER"
echo "Remarque : Fedora utilise souvent Podman comme solution rootless. Ce script installe Docker Engine classique." 
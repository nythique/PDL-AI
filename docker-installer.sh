#!/bin/bash
#------------------------------------------------------------------
# Simple Docker installer for Fedora
# - checks OS
# - installs prerequisites
# - adds Docker repo (via config-manager or fallback to curl)
# - installs Docker packages and starts the service
# - adds current user to 'docker' group
# Usage: sudo bash docker-installer.sh
#------------------------------------------------------------------

set -euo pipefail

echo "== Vérification de l'OS =="
if [ -f /etc/os-release ]; then
    . /etc/os-release
else
    echo "Impossible de détecter le système (/etc/os-release manquant)." >&2
    exit 1
fi

if [ "${ID:-}" != "fedora" ]; then
    echo "Attention : ce script est prévu pour Fedora (OS détecté : ${ID:-unknown})." >&2
    read -r -p "Continuer quand même ? (y/N) " answer
    if [[ "${answer,,}" != "y" ]]; then
        echo "Annulation."; exit 1
    fi
fi

echo "== Mise à jour du système =="
sudo dnf -y upgrade --refresh

echo "== Installation des dépendances de base =="
sudo dnf install -y dnf-plugins-core ca-certificates curl gnupg

echo "== Ajout du dépôt Docker (tentative via config-manager) =="
if sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo 2>/dev/null; then
    echo "Dépôt ajouté via config-manager."
else
    echo "config-manager indisponible ou option non supportée — écriture manuelle du fichier .repo"
    sudo curl -fsSL https://download.docker.com/linux/fedora/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
    echo "Fichier /etc/yum.repos.d/docker-ce.repo écrit."
fi

echo "== Mise à jour du cache des paquets =="
sudo dnf makecache

echo "== Installation de Docker Engine =="
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "== Activation et démarrage du service Docker =="
sudo systemctl enable --now docker
sudo systemctl status --no-pager --full docker || true

echo "== Ajout de l'utilisateur courant au groupe 'docker' =="
sudo usermod -aG docker "$USER"

echo "== Terminé =="
echo "Relancez votre session (déconnexion/connexion) ou exécutez: newgrp docker"
echo "Test: docker run hello-world"
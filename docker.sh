#!/bin/bash
#==================================================================
# docker.sh - Script to install Docker on Ubuntu
# This script is intended for Ubuntu systems and requires sudo privileges.
# Ensure the script is run with root privileges
# Usage: ./docker.sh
# Author: nythique
# License: GNU AFFERO GENERAL PUBLIC LICENSE
# Version: 1.0
# Date: 2025-07-18
#==================================================================

set -e

echo "==================🚀 Mise à jour du système...=================="
sudo apt update && sudo apt upgrade -y

echo "📦 Installation des dépendances Docker..."
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
clear
echo "==================🔐 Ajout de la clé GPG Docker...=================="
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
clear
echo "==================📦 Ajout du dépôt Docker à APT...=================="
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
clear
echo "==================🔄 Mise à jour des paquets avec dépôt Docker...=================="
sudo apt update
clear
echo "==================🐳 Installation de Docker Engine...=================="
sudo apt install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
clear
echo "==================👤 Ajout de l'utilisateur $USER au groupe docker...=================="
sudo usermod -aG docker $USER
clear
echo "==================✅ Docker est installé. Pour lancer le daemon :=================="
echo "    sudo dockerd &"
echo "Et ensuite, dans un autre terminal :"
echo "    docker run hello-world"
echo ""
echo "⚠️ Remarque : Redémarre ton terminal ou tape 'newgrp docker' pour activer le groupe docker sans déconnexion."
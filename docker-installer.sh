#!/bin/bash
#------------------------------------------------------------------
# Automated Docker installer for Fedora
# - fully automated: non-interactive by default (use --no-auto to prompt)
# - handles repo addition (config-manager or fallback)
# - resolves package conflicts automatically using --allowerasing
# - logs to /var/log/pdl-docker-installer.log
# Usage: sudo bash docker-installer.sh [--yes|-y] [--no-auto]
#------------------------------------------------------------------

set -euo pipefail

LOG=/var/log/pdl-docker-installer.log
AUTO=1

for arg in "$@"; do
  case "$arg" in
    --yes|-y) AUTO=1 ;; 
    --no-auto) AUTO=0 ;;
    --help|-h)
      echo "Usage: sudo bash docker-installer.sh [--yes|-y] [--no-auto]";
      exit 0;;
  esac
done

# Ensure log file exists and is writable
sudo mkdir -p "$(dirname "$LOG")"
sudo touch "$LOG"
sudo chown "$SUDO_USER":"$SUDO_USER" "$LOG" 2>/dev/null || true

# tee all output to log (requires running with sudo to write /var/log)
exec > >(tee -a "$LOG") 2>&1

echo "=== PDL Docker installer started: $(date -u) ==="

echo "== Vérification de l'OS =="
if [ -f /etc/os-release ]; then
    . /etc/os-release
else
    echo "Impossible de détecter le système (/etc/os-release manquant)." >&2
    exit 1
fi

if [ "${ID:-}" != "fedora" ]; then
    echo "Attention : OS détecté = ${ID:-unknown} (script prévu pour Fedora)."
    if [ "$AUTO" -eq 1 ]; then
        echo "Mode automatique activé, on continue quand même."
    else
        read -r -p "Continuer quand même ? (y/N) " answer
        if [[ "${answer,,}" != "y" ]]; then
            echo "Annulation."; exit 1
        fi
    fi
fi

echo "== Mise à jour du système =="
sudo dnf -y upgrade --refresh

echo "== Installation des dépendances de base =="
sudo dnf install -y dnf-plugins-core ca-certificates curl gnupg || true

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

echo "== Pré-check: Docker déjà installé ? =="
if command -v docker >/dev/null 2>&1; then
    echo "Docker détecté : $(docker --version || true). Nous allons tenter de mettre à jour/aligner si besoin."
fi

echo "== Installation de Docker Engine (résolution automatique des conflits) =="
# Use --allowerasing to allow DNF to remove conflicting packages (moby, docker from fedora)
if sudo dnf install -y --allowerasing docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; then
    echo "Packages Docker installés/à jour."
else
    echo "Installation avec --allowerasing a échoué. Tentative de suppression manuelle des paquets conflictuels."
    echo "Liste des paquets potentiellement conflictuels : moby-engine docker docker-cli docker-compose"
    sudo dnf remove -y moby-engine docker docker-cli docker-compose || true
    echo "Ré-essai d'installation Docker CE..."
    sudo dnf install -y --allowerasing docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

echo "== Activation et démarrage du service Docker =="
sudo systemctl enable --now docker
sudo systemctl status --no-pager --full docker || true

echo "== Ajout de l'utilisateur courant au groupe 'docker' =="
# If SUDO_USER is set, add that user; otherwise add current user
TARGET_USER=${SUDO_USER:-$USER}
sudo usermod -aG docker "$TARGET_USER" || true

echo "== Nettoyage/cache =="
sudo dnf makecache || true

echo "=== FIN: $(date -u) ==="
echo "Relancez la session pour $TARGET_USER (déconnexion/connexion) ou exécutez: newgrp docker"
echo "Test: docker run hello-world (après relogin/newgrp)"
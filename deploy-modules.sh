#!/bin/bash
# Généré et copié dans le répertoire Odoo par deploy.sh (étape 8) — les
# placeholders __...__ sont substitués à la copie. Ne pas éditer la copie
# déployée directement, éditer ce fichier dans le repo puis re-déployer.
set -euo pipefail

readonly DEFAULT_DEPLOY_SSH_KEY="$HOME/.ssh/id_ed25519_github"
DEPLOY_SSH_KEY="${DEPLOY_SSH_KEY:-}"
DEPLOY_SSH_KEY="${DEPLOY_SSH_KEY:-$DEFAULT_DEPLOY_SSH_KEY}"

REPO_DIR="__REPO_DIR__"
ADDONS_DIR="__ADDONS_DIR__"
ADDON_MODULES=(oaas_website_addons oaas_linkedin_addons)
ODOO_OWNER="__ODOO_OWNER__"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

export GIT_SSH_COMMAND="ssh -i ${DEPLOY_SSH_KEY} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

log "Récupération des sources depuis le dépôt Git..."
git -C "${REPO_DIR}" pull --ff-only

log "Déploiement des modules OAAS..."
for module in "${ADDON_MODULES[@]}"; do
    sudo rm -rf "${ADDONS_DIR}/${module}"
    sudo cp -r "${REPO_DIR}/${module}" "${ADDONS_DIR}/"
done
sudo chown -R "${ODOO_OWNER}" "${ADDONS_DIR}"

log "Redémarrage du service Odoo..."
sudo systemctl restart odoo

log "Déploiement terminé."

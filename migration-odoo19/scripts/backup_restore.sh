#!/usr/bin/env bash
# Backup / restore DB + filestore Odoo, à exécuter avant toute opération de
# migration ou de déploiement (voir migration-odoo19/03-risques-infra.md,
# section "Absence de backup/restore automatisé").
#
# Ne contient aucun secret : le mot de passe PostgreSQL est lu via .pgpass
# ou la variable d'environnement PGPASSWORD, jamais en dur dans ce script.
#
# Usage :
#   ODOO_DB=oaas ODOO_FILESTORE=/var/lib/odoo/.local/share/Odoo/filestore/oaas \
#     ./backup_restore.sh backup /chemin/vers/dossier_backup
#
#   ODOO_DB=oaas ODOO_FILESTORE=/var/lib/odoo/.local/share/Odoo/filestore/oaas \
#     ./backup_restore.sh restore /chemin/vers/dossier_backup
#
# ODOO_FILESTORE dépend de l'environnement cible (data_dir dans odoo.conf) —
# vérifier la valeur réelle avant le premier usage, la valeur par défaut
# ci-dessous est indicative.

set -euo pipefail

ACTION="${1:?Usage: $0 backup|restore <dossier>}"
TARGET_DIR="${2:?Usage: $0 backup|restore <dossier>}"

ODOO_DB="${ODOO_DB:?Variable ODOO_DB requise (nom de la base Odoo)}"
ODOO_DB_HOST="${ODOO_DB_HOST:-localhost}"
ODOO_DB_PORT="${ODOO_DB_PORT:-5432}"
ODOO_DB_USER="${ODOO_DB_USER:-odoo}"
ODOO_FILESTORE="${ODOO_FILESTORE:-$HOME/.local/share/Odoo/filestore/$ODOO_DB}"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

backup() {
    mkdir -p "$TARGET_DIR"
    local dump_file="$TARGET_DIR/${ODOO_DB}_${TIMESTAMP}.dump"
    local filestore_archive="$TARGET_DIR/${ODOO_DB}_filestore_${TIMESTAMP}.tar.gz"

    echo "-> pg_dump ($ODOO_DB@$ODOO_DB_HOST:$ODOO_DB_PORT) vers $dump_file"
    pg_dump -h "$ODOO_DB_HOST" -p "$ODOO_DB_PORT" -U "$ODOO_DB_USER" \
        -F custom -f "$dump_file" "$ODOO_DB"

    if [ -d "$ODOO_FILESTORE" ]; then
        echo "-> archive filestore ($ODOO_FILESTORE) vers $filestore_archive"
        tar -czf "$filestore_archive" -C "$(dirname "$ODOO_FILESTORE")" "$(basename "$ODOO_FILESTORE")"
    else
        echo "!! filestore introuvable à $ODOO_FILESTORE — dump DB seul, à vérifier" >&2
    fi

    echo "-> backup terminé : $dump_file"
    [ -f "$filestore_archive" ] && echo "                     $filestore_archive"
}

restore() {
    local dump_file
    local filestore_archive
    dump_file="$(ls -t "$TARGET_DIR"/${ODOO_DB}_*.dump 2>/dev/null | head -n1)"
    filestore_archive="$(ls -t "$TARGET_DIR"/${ODOO_DB}_filestore_*.tar.gz 2>/dev/null | head -n1)"

    [ -n "$dump_file" ] || { echo "Aucun dump trouvé dans $TARGET_DIR" >&2; exit 1; }

    echo "!! Cette opération écrase la base '$ODOO_DB' et son filestore."
    read -r -p "Confirmer la restauration depuis $dump_file ? [oui/N] " confirm
    [ "$confirm" = "oui" ] || { echo "Annulé."; exit 1; }

    echo "-> dropdb / createdb $ODOO_DB"
    dropdb -h "$ODOO_DB_HOST" -p "$ODOO_DB_PORT" -U "$ODOO_DB_USER" --if-exists "$ODOO_DB"
    createdb -h "$ODOO_DB_HOST" -p "$ODOO_DB_PORT" -U "$ODOO_DB_USER" "$ODOO_DB"

    echo "-> pg_restore depuis $dump_file"
    pg_restore -h "$ODOO_DB_HOST" -p "$ODOO_DB_PORT" -U "$ODOO_DB_USER" \
        -d "$ODOO_DB" "$dump_file"

    if [ -n "$filestore_archive" ]; then
        echo "-> restauration filestore depuis $filestore_archive vers $ODOO_FILESTORE"
        rm -rf "$ODOO_FILESTORE"
        mkdir -p "$(dirname "$ODOO_FILESTORE")"
        tar -xzf "$filestore_archive" -C "$(dirname "$ODOO_FILESTORE")"
    else
        echo "!! aucune archive filestore trouvée dans $TARGET_DIR — DB seule restaurée" >&2
    fi

    echo "-> restauration terminée"
}

case "$ACTION" in
    backup)  backup ;;
    restore) restore ;;
    *) echo "Action inconnue: $ACTION (attendu: backup|restore)" >&2; exit 1 ;;
esac

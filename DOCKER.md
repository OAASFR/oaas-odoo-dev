# Déploiement Docker (Windows 11)

Stack : Odoo 16 + PostgreSQL 15 via Docker Compose. Les addons OAAS sont montés en volume (modifs visibles sans rebuild, redémarrer le module suffit).

## Fichiers

- `Dockerfile` — image Odoo 16 + deps Python des addons (`openpyxl`, `translate`, `nltk` + données `punkt`).
- `docker-compose.yml` — services `odoo` et `db`.
- `odoo.conf` — config Odoo (pointe vers le service `db`).

## Démarrer

```powershell
docker compose up -d --build
```

Puis ouvrir http://localhost:8069

Au premier lancement, créer une base de données (mot de passe maître = `admin`, défini dans `odoo.conf`), puis installer le module **oaas_website_addons** depuis Apps.

## Commandes utiles

```powershell
docker compose logs -f odoo          # suivre les logs
docker compose restart odoo          # redémarrer Odoo
docker compose down                  # arrêter (garde les données)
docker compose down -v               # arrêter ET supprimer les données

# Mettre à jour un module après modif XML/Python
docker compose exec odoo odoo -u oaas_website_addons -d <nom_base> --stop-after-init
docker compose restart odoo
```

## Notes

- Données persistées dans les volumes Docker `db-data` (PostgreSQL) et `odoo-data` (filestore).
- Pour la prod, changer `admin_passwd` dans `odoo.conf` et le mot de passe PostgreSQL dans `docker-compose.yml` + `odoo.conf`.
- `deploy.sh` est l'ancien déploiement bare-metal Linux (systemd/Apache) — non utilisé par Docker.

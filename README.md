# odoo-oaas-addons

Addons Odoo 16.0 personnalisés pour **O.A.A.S.** ([oaas.fr](https://oaas.fr/)).

## Modules

| Module | Statut | Description |
|---|---|---|
| [`oaas_website_addons`](oaas_website_addons/README.md) | Actif | Import d'articles de blog (Excel bilingue EN/FR), snippet builder `s_oaas_tech`, fichiers `llms.txt`. |
| [`oaas_linkedin_addons`](oaas_linkedin_addons/README.md) | Actif | Publication des articles de blog sur la page entreprise LinkedIn (action manuelle, OAuth). |
| [`oaas_docusign_addons`](oaas_docusign_addons/README.md) | Scaffold | Intégration DocuSign — non implémentée. |

## Environnement serveur

| Élément | Valeur |
|---|---|
| Installation Odoo | `/var/www/html/odoo/` |
| Fichier de config | `/var/www/html/odoo/odoo.conf` |
| Chemin d'addons | `/var/www/html/odoo/odoo-oaas-addons,/var/www/html/odoo/addons` |
| Log | `/var/www/html/odoo/log/odoo-server.log` |
| Base | PostgreSQL `oaas` sur `localhost:5432`, utilisateur `odoo` |
| Service systemd | `odoo.service` |

Le dossier d'addons du serveur est un **clone git** de ce dépôt :
déployer = `git pull` dans ce dossier, puis mise à jour du module concerné.

## Développement local (Docker)

`docker-compose.yml` monte chaque module dans un conteneur Odoo 16 + Postgres :

```bash
# Démarrer / reconstruire (après modif du Dockerfile)
docker compose up -d --build

# Installer un module
docker compose exec odoo odoo -d oaas -i oaas_linkedin_addons --stop-after-init
docker compose restart odoo

# Mettre à jour un module après modif Python/XML
docker compose exec odoo odoo -d oaas -u oaas_website_addons --stop-after-init
```

Odoo est exposé sur http://localhost:8069. Détails dans [DOCKER.md](DOCKER.md).

Chaque nouveau module doit être :
1. ajouté comme volume dans `docker-compose.yml` (`./<module>:/mnt/extra-addons/<module>:ro`) ;
2. accompagné de ses dépendances Python dans le `Dockerfile` si nécessaire.

## Commandes serveur courantes

```bash
# Redémarrer le service (après toute modif Python/XML)
sudo systemctl restart odoo

# Suivre le log
tail -f /var/www/html/odoo/log/odoo-server.log

# Mettre à jour un module sans full restart
/var/www/html/odoo/.venv/bin/python3 /var/www/html/odoo/odoo-bin \
  --config=/var/www/html/odoo/odoo.conf \
  -u oaas_website_addons --stop-after-init
```

## Déploiement

Le script [`deploy.sh`](deploy.sh) provisionne une install complète (clone Odoo,
venv, dépendances, service systemd, Apache) et copie les addons. Pour une simple
mise à jour de code sur un serveur déjà provisionné, préférer `git pull` + mise
à jour du module concerné.

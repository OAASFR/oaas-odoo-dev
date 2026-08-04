# Risques d'infrastructure

Points à régler avant de pouvoir migrer sereinement — indépendants du code
des modules, mais bloquants pour une migration sans risque.

## Absence de staging Odoo

`deploy.sh` provisionne directement le serveur décrit dans le `CLAUDE.md`
du repo, et les callbacks OAuth LinkedIn en "prod" pointent vers `oaas.fr`.
Contrairement au reste de l'infra OAAS (`validation.*.oaas.fr`), il
n'existe aucun environnement de validation dédié à Odoo.

**Recommandation** : cloner la base de données et le filestore de
production vers un environnement Odoo isolé (VM ou conteneur séparé, DB
distincte) avant toute manipulation liée à la migration. Ne jamais migrer
en place sur le serveur de production.

## Absence de backup/restore automatisé

`deploy.sh` ne contient aucune commande `pg_dump`/`pg_restore` ni logique
de rollback. Il se contente de cloner/patcher le code, redémarrer le
service et reconfigurer Apache, sans jamais toucher aux données.

**Recommandation** : ajouter un script de sauvegarde (DB + filestore) avec
procédure de restauration testée, à exécuter systématiquement avant toute
opération de migration ou de déploiement — même hors du cadre de cette
migration Odoo 19.

**État** : script préparé dans [`scripts/backup_restore.sh`](scripts/backup_restore.sh)
(`backup`/`restore`, `pg_dump -F custom` + archive filestore, confirmation
explicite requise avant tout `restore` destructif, aucun secret en dur —
mot de passe PostgreSQL lu via `.pgpass`/`PGPASSWORD`). **Non testé** : pas
d'environnement Odoo/PostgreSQL disponible sur cette VM pour valider un
cycle backup→restore réel. Le chemin `ODOO_FILESTORE` par défaut est
indicatif — à vérifier contre la valeur réelle de `data_dir` sur le serveur
cible avant le premier usage.

## Secrets en clair

Le mot de passe PostgreSQL généré par `deploy.sh` est en clair dans le
script (`Maison63#123`), ainsi que l'`admin_passwd` de la config Docker
locale (`odoo.conf` du repo, `admin_passwd = admin`).

**Recommandation** : externaliser ces secrets (variables d'environnement,
fichier non versionné) avant de retravailler `deploy.sh` pour la cible
Odoo 19.

## Deux chaînes de déploiement divergentes

- Docker local : `odoo:16.0` + `postgres:15`, `workers = 0` (mode dev
  mono-process), utilisé sur poste Windows de dev.
- Bare-metal (`deploy.sh`) : `workers = 8` (mode prod multi-process),
  reverse-proxy Apache, service systemd — c'est la chaîne qui patche Odoo
  16 pour Python 3.13/3.14.

Ces deux environnements ne se comportent pas de la même façon (nombre de
workers, limites mémoire, mode proxy). Tester uniquement en local Docker
ne garantit pas un comportement identique en bare-metal.

**Recommandation** : avant la migration, aligner les deux chaînes (ou au
minimum documenter précisément leurs différences) pour que
l'environnement de test Odoo 19 soit représentatif de la cible réelle.

## Python déjà en avance sur ce qu'Odoo 16 supporte officiellement

`deploy.sh` contient une section de patches (lignes ~134-200) qui modifie
directement le code source d'Odoo 16 (`safe_eval.py`, `ir_qweb.py`,
`view_validation.py`, `ir_ui_view.py`) pour gérer des opcodes bytecode
Python 3.13/3.14 et remplacer `ast.Str` (déprécié) par `ast.Constant`.
Odoo 16 ne supporte officiellement que Python jusqu'à 3.10.

C'est probablement le signal le plus fort en faveur de cette migration :
le serveur tourne déjà sur un Python plus récent que ce qu'Odoo 16 est
censé supporter, via des patches maison fragiles. Odoo 19 supportera
nativement ces versions de Python, ce qui supprimera le besoin de ces
patches.

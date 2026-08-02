# Migration Odoo 16 → Odoo 19

Ce dossier centralise la préparation de la migration des addons custom
OAAS (`oaas_website_addons`, `oaas_docusign_addons`, `oaas_linkedin_addons`)
d'Odoo 16.0 vers Odoo 19.0.

## Trajectoire

La migration est **obligatoirement séquentielle** : 16 → 17 → 18 → 19.
Il n'est pas possible de sauter une version majeure — les scripts de
migration de schéma de chaque palier dépendent des transformations du
palier précédent (le passage 18→19 seul applique environ 300 scripts qui
supposent que les transformations 17→18 ont déjà eu lieu).

## Périmètre de cette documentation

Ces fichiers sont une **préparation** (inventaire technique + checklist),
pas une exécution. Aucune modification n'a été faite au code des modules
ni à l'infrastructure de déploiement. L'exécution réelle (upgrade des
modules, tests sur environnement réel, bascule du serveur) se fera plus
tard, manuellement ou via une session `/projet` dédiée, une fois qu'un
environnement de test isolé existera (voir `03-risques-infra.md` —
c'est aujourd'hui le principal point bloquant).

**Important** : il n'existe actuellement aucun environnement de
validation/staging dédié à Odoo (contrairement au reste de l'infra OAAS
qui utilise `validation.*.oaas.fr`). `deploy.sh` provisionne directement
ce qui semble être le serveur de production (`oaas.fr`). Tant que ce point
n'est pas réglé, aucune étape de cette migration ne doit être exécutée
directement sur ce serveur.

## Sommaire

- [`01-inventaire-technique.md`](01-inventaire-technique.md) — état des lieux
  du code existant, module par module, avec les points qui casseront lors
  de la migration.
- [`02-checklist-migration.md`](02-checklist-migration.md) — checklist
  ordonnée par palier de version, à cocher au fur et à mesure du travail
  réel.
- [`03-risques-infra.md`](03-risques-infra.md) — risques d'infrastructure
  à traiter avant de pouvoir migrer sereinement (absence de staging, de
  backup, secrets en clair).

# Palier 17.0 → 18.0 — code préparé

Copies patchées de `oaas_website_addons` et `oaas_linkedin_addons`, partant
du code déjà préparé dans `../palier16-17/` (les fixes 16→17 sont donc déjà
présents ici en plus des fixes 17→18 ci-dessous). Prêtes à être installées
sur un Odoo 18.0 une fois un environnement de test isolé disponible (voir
`../03-risques-infra.md`).

Comme pour le palier précédent : préparation de code, aucune exécution
réelle, rien touché sur les modules à la racine du repo ni sur un serveur.

## Changements appliqués (en plus de ceux de `../palier16-17/`)

- `oaas_website_addons/views/views.xml` — `<tree>` → `<list>`, et les deux
  occurrences `view_mode: "tree,form"` → `"list,form"`
  (`blog_post_import_action_windows` + action serveur)
- `oaas_linkedin_addons/controllers/linkedin_oauth.py:86` —
  `werkzeug.utils.escape()` → `markupsafe.escape()` (supprimé de Werkzeug
  ≥ 2.1, aurait fait crasher le contrôleur OAuth au chargement)
- `oaas_linkedin_addons/data/ir_actions_server.xml` — vérifié :
  `binding_view_types="list,form"` était **déjà** correct dans le code
  source (pas `tree,form`), aucun changement nécessaire ici
- `__manifest__.py` des deux modules : `version` bump vers `18.0.x.y.z`
- Squelette `migrations/18.0.x.y.z/post-migrate.py` dans les deux modules —
  même logique no-op documentée que pour le palier précédent

## Non couvert ici (hors scope de ce palier)

- Vérification de la restructuration du bundling d'assets — impact attendu
  faible (aucun module ne déclare de clé `assets` dans son manifeste
  aujourd'hui), à reconfirmer si du JS est ajouté avant la migration
  effective
- `odoo-bin -u <module> --test-enable` — nécessite l'environnement de test
  qui n'existe pas encore

## Vérifications faites sur ce code préparé

- Tous les XML sont bien formés (`xml.dom.minidom`)
- Tous les fichiers Python compilent (`py_compile`)
- Pas de compilation/exécution réelle possible : nécessite un Odoo 18
  installé + une base de données, absents de cette VM

## Utilisation prévue

Même procédure que `../palier16-17/README.md`, sur un environnement Odoo 18.

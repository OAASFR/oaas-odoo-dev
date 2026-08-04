# Palier 16.0 → 17.0 — code préparé

Copies patchées de `oaas_website_addons` et `oaas_linkedin_addons`, prêtes à
être installées sur un Odoo 17.0 **une fois un environnement de test isolé
disponible** (voir `../03-risques-infra.md` — point bloquant non résolu à ce
jour). `oaas_docusign_addons` n'est pas dupliqué ici : c'est un scaffold vide,
sans rien à migrer avant implémentation (voir `../01-inventaire-technique.md`).

Ce dossier est une **préparation de code**, pas une exécution. Rien n'a été
appliqué aux modules réels à la racine du repo, ni à un serveur.

## Changements appliqués (par rapport au code 16.0 à la racine du repo)

- `oaas_website_addons/views/res_config_settings_views.xml:65` —
  `attrs=` → `invisible="oaas_llms_mode != 'manual'"`
- `oaas_linkedin_addons/views/blog_post_views.xml:15,24,36,38` — 4 occurrences
  `attrs=` → `invisible=` inline
- `oaas_linkedin_addons/views/res_config_settings_views.xml:55,60` — 2
  occurrences `attrs=` → `invisible=` inline
- `__manifest__.py` des deux modules : `version` bump vers `17.0.x.y.z`
  (préfixe Odoo manquant dans le code source actuel)
- Squelette `migrations/17.0.x.y.z/post-migrate.py` dans les deux modules —
  no-op documenté : aucune transformation de donnée identifiée pour ce
  palier (voir commentaire en tête de chaque fichier), prêt si un besoin
  apparaît plus tard

## Non couvert ici (hors scope de ce palier)

- Retest visuel du snippet `s_oaas_tech` et des pages `res.config.settings`
  (builder de vues refondu en 17) — nécessite un environnement Odoo réel,
  pas faisable en préparation de code statique
- `odoo-bin -u <module> --test-enable` — nécessite l'environnement de test
  qui n'existe pas encore
- Dette générale non gated par un palier précis (SQL brut, `Pillow` absent
  d'`external_dependencies`, code mort) — volontairement laissée de côté ici
  pour rester strictement sur le scope 16→17, voir
  `../01-inventaire-technique.md`

## Vérifications faites sur ce code préparé

- Tous les XML sont bien formés (`xml.dom.minidom`)
- Tous les fichiers Python compilent (`py_compile`)
- Pas de compilation/exécution réelle possible : nécessite un Odoo 17
  installé + une base de données, absents de cette VM

## Utilisation prévue

Une fois l'environnement de test isolé en place (voir
`../scripts/backup_restore.sh` pour sauvegarder avant toute manipulation) :
copier le contenu de ce dossier vers l'`addons_path` Odoo 17, lancer
`-u oaas_website_addons,oaas_linkedin_addons --test-enable`, puis dérouler
les retests visuels listés ci-dessus.

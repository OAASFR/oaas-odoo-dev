# Checklist de migration Odoo 16 → 19

À cocher au fur et à mesure. Ordonnée par palier — respecter l'ordre,
la trajectoire est séquentielle (16→17→18→19).

**Code préparé** : les fixes des paliers 1 et 2 sont écrits et vérifiés
statiquement (XML bien formés, Python compile) dans
[`palier16-17/`](palier16-17/) et [`palier17-18/`](palier17-18/) — voir leurs
README respectifs pour le détail. Les cases ci-dessous restent décochées
tant qu'elles n'ont pas été **exécutées sur un environnement Odoo réel**
(`--test-enable`, retests visuels) : écrire le code n'est pas la même chose
que le valider en conditions réelles, et aucun environnement de test isolé
n'existe à ce jour (voir `0. Prérequis infra`).

## 0. Prérequis infra (bloquant avant tout code)

- [ ] Environnement de test isolé (clone de la DB + filestore de prod,
      **jamais migrer en place sur le serveur de production**)
- [ ] Script de sauvegarde (`pg_dump` + filestore) avant toute opération,
      avec procédure de restauration testée — préparé dans
      [`scripts/backup_restore.sh`](scripts/backup_restore.sh), **non
      encore testé faute d'environnement**
- [ ] Secrets sortis de `deploy.sh` en clair (mot de passe PostgreSQL) vers
      un mécanisme de variables d'environnement / secret manager
- [ ] Chaîne de déploiement unifiée (Docker vs bare-metal) pour que
      l'environnement de test représente fidèlement la cible réelle

## 1. Palier 16 → 17

- [ ] `oaas_website_addons/views/res_config_settings_views.xml:65` —
      `attrs=` → `invisible="oaas_llms_mode != 'manual'"`
- [ ] `oaas_linkedin_addons/views/blog_post_views.xml:15,24,36,38` —
      6 occurrences `attrs=` → expressions Python inline
- [ ] `oaas_linkedin_addons/views/res_config_settings_views.xml:55,60` —
      idem
- [ ] Retest visuel du snippet `s_oaas_tech` dans l'éditeur de site
      (builder de snippets refondu en 17 — xpath sur `#snippet_feature`
      à revérifier)
- [ ] Retest visuel des pages `res.config.settings` (Website et LinkedIn)
- [ ] `odoo-bin -u <module> --test-enable` sur les 3 modules,
      environnement de test

## 2. Palier 17 → 18

- [ ] `<tree>` → `<list>` : `oaas_website_addons/views/views.xml`
- [ ] Vérifier `binding_view_types="list,form"` dans
      `oaas_linkedin_addons/data/ir_actions_server.xml:8,21` après le
      renommage
- [ ] `oaas_linkedin_addons/controllers/linkedin_oauth.py:86` —
      `werkzeug.utils.escape()` → `markupsafe.escape()` (supprimé en
      Werkzeug ≥ 2.1)
- [ ] Vérifier la restructuration du bundling d'assets (impact attendu
      faible : aucun module ne déclare de clé `assets` dans son manifeste
      aujourd'hui — à reconfirmer si du JS est ajouté avant la migration)
- [ ] `odoo-bin -u <module> --test-enable` sur les 3 modules

## 3. Palier 18 → 19

Palier le plus lourd (130 renommages de modèles, 416 changements de
contraintes, 51 renommages de champs côté core Odoo).

- [ ] Vérifier le changelog officiel Odoo 19 pour tout champ/modèle core
      référencé par les modules : `blog.post`, `res.config.settings`,
      `website.snippets`
- [ ] Vérifier `security/ir.model.access.csv` des 3 modules si des groupes
      de sécurité custom existent (changement `res.groups` →
      `privilege_id`/`group_ids` en 19 — pas d'usage direct identifié
      aujourd'hui, à reconfirmer)
- [ ] `odoo-bin -u <module> --test-enable` sur les 3 modules

## 4. Par module (rappel — détail dans `01-inventaire-technique.md`)

- [ ] `oaas_website_addons` : durcir le SQL brut par concaténation
      (`models/models.py:76-77`), ajouter `Pillow` aux
      `external_dependencies`, nettoyer le code mort (hooks commentés)
- [ ] `oaas_docusign_addons` : rien à faire tant que le module reste vide —
      juste bump `version`/`depends` si implémenté après coup
- [ ] `oaas_linkedin_addons` : mettre à jour `CLAUDE.md` du repo pour
      documenter ce module (actuellement absent), ajouter des tests sur le
      flux OAuth du contrôleur et `upload_image`/`create_post`

## 5. Validation finale (environnement de test Odoo 19)

- [ ] Réinstallation propre des 3 modules sur l'environnement de test 19
- [ ] Exécution des 21 tests automatisés existants
      (`oaas_linkedin_addons/tests/`)
- [ ] Test manuel du flux OAuth LinkedIn complet (non couvert par les
      tests automatisés)
- [ ] Test manuel de l'import blog Excel bilingue EN/FR (wizard
      `blog.post.import`)
- [ ] Test manuel de publication + republication LinkedIn (smart buttons)
- [ ] Test manuel du résumé IA (Ollama) sur un article réel
- [ ] Validation du snippet `s_oaas_tech` dans l'éditeur de site

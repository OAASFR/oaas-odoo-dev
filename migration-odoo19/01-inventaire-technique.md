# Inventaire technique (état au 2026-08-03)

Inventaire du code des 3 modules du repo, avec les points identifiés comme
candidats à breaking change sur la trajectoire Odoo 16 → 19.

## `oaas_website_addons`

Import de blog Excel bilingue EN/FR (wizard `blog.post.import`), builder de
LLMs.txt (`oaas.llms.builder`), snippet website `s_oaas_tech`.

- **`attrs=` à corriger** (supprimé en Odoo 17) :
  `views/res_config_settings_views.xml:65`
  ```xml
  attrs="{'invisible': [('oaas_llms_mode', '!=', 'manual')]}"
  ```
  → à réécrire `invisible="oaas_llms_mode != 'manual'"`.
- **SQL brut par concaténation de chaîne** (`models/models.py:76-77`) :
  écrit le JSON bilingue `blog_post.content` en contournant l'ORM, sans
  paramètres bindés. Pas une dépréciation Odoo à proprement parler, mais à
  corriger à l'occasion de la migration (fragile, risque d'injection si la
  source de données change un jour).
- **Dépendance à la structure DOM interne de `website.snippets`**
  (`views/templates.xml:137-141`, xpath sur `#snippet_feature`) et de
  `website.res_config_settings_view_form`
  (`views/res_config_settings_views.xml:10`) : le builder de snippets a été
  largement refondu en Odoo 17 (nouveau système d'onglets/catégories) — à
  **retester visuellement**, pas seulement à corriger du code.
- **`<tree>` → `<list>`** : `views/views.xml` utilise encore `<tree>`.
  Alias conservé un temps en 17/18 mais officiellement renommé — à migrer
  au palier 18.
- **Aucun JS** dans tout le module — pas de risque OWL/assets sur ce
  module, la bascule frontend est déjà "gratuite" ici.
- **Dépendances externes** : `Pillow` (`PIL.Image`) utilisée mais absente
  d'`external_dependencies` dans `__manifest__.py` — à corriger
  indépendamment de la migration.
- Divers : hooks `pre_init_hook`/`post_init_hook` commentés mais
  `scripts/oaas_website_addons_init.py` toujours importé (code mort à
  nettoyer), `version: '0.2'` sans préfixe de version Odoo (`16.0.x.y.z`).

## `oaas_docusign_addons`

**Scaffold vide** — tout le code (`models/models.py`,
`controllers/controllers.py`, vues, démo) est commenté, aucun modèle actif.
`security/ir.model.access.csv` référence un modèle inexistant (fichier
orphelin, jamais chargé).

→ Rien à migrer techniquement. Le jour où ce module sera implémenté, mettre
directement à jour `'version'` et `'depends'` vers la cible `19.0.x.y.z` —
pas besoin de suivre la trajectoire 16→17→18 puisqu'il n'y a pas de code
existant à faire évoluer version par version.

## `oaas_linkedin_addons`

Publication automatique + résumé IA (Ollama) des articles de blog vers
LinkedIn, OAuth2 complet, republication volontaire.

- **6 occurrences `attrs=` à corriger** :
  `views/blog_post_views.xml:15,24,36,38` (smart buttons "Publier"/
  "Republier"), `views/res_config_settings_views.xml:55,60` (statut
  connecté/non connecté).
- **`werkzeug.utils.escape()` supprimé dans Werkzeug ≥ 2.1**
  (`controllers/linkedin_oauth.py:86`) — Odoo 16 embarque encore une
  version de Werkzeug qui le supporte, mais 17/18/19 montent la version en
  dépendance. **À remplacer par `markupsafe.escape` avant la traversée
  17→18**, sinon crash au chargement du contrôleur.
- **`binding_view_types="list,form"`** sur les `ir.actions.server`
  (`data/ir_actions_server.xml:8,21`) — à revérifier après le renommage
  `<tree>`→`<list>` du palier 18, que le binding s'attache toujours
  correctement.
- **Credentials déjà proprement isolés** : tokens LinkedIn (access/refresh)
  et clé API Ollama stockés en `ir.config_parameter` via `sudo()`, jamais
  en dur dans le code ni exposés dans un champ de formulaire classique —
  rien à durcir côté secrets pour la migration elle-même.
- **Tests** (`tests/`, 21 tests au total, mocks HTTP via
  `unittest.mock.patch`, aucun appel réseau réel) :
  `test_ai_summarizer.py` (10), `test_res_config_settings.py` (3),
  `test_blog_post_linkedin.py` (4), `test_linkedin_client.py` (4). Bonne
  couverture de la logique métier, mais **le flux OAuth du contrôleur
  (`linkedin_oauth.py`) et `upload_image`/`create_post` du client ne sont
  pas testés directement** — à tester manuellement après chaque palier.
- Divers : `__init__.py` importe `tests` inconditionnellement (pattern non
  standard, sans risque connu mais à surveiller si le chargeur d'addons
  change), module absent du `CLAUDE.md` du repo (décalage doc à corriger),
  `version: '0.1'` sans préfixe `16.0.`.

## Infrastructure

- **`deploy.sh` patche déjà le code source d'Odoo 16** (`safe_eval.py`,
  `ir_qweb.py`, `view_validation.py`, `ir_ui_view.py`) pour tourner sur
  Python 3.13/3.14 (opcodes bytecode récents, `ast.Str`→`ast.Constant`).
  Signe que le serveur cible tourne sur un Python plus récent que celui
  officiellement supporté par Odoo 16 — probable motivation de cette
  migration.
- **Deux chaînes de déploiement divergentes** : Docker local
  (`odoo:16.0` + `postgres:15`, `workers=0`, mode dev) vs bare-metal
  `deploy.sh`/systemd (`workers=8`, mode prod). Configs `odoo.conf`
  différentes, à unifier avant la migration pour éviter de tester sur un
  environnement qui ne représente pas la cible réelle.
- **Mot de passe PostgreSQL en clair** dans `deploy.sh`
  (`Maison63#123`) — à traiter en priorité de sécurité, indépendamment de
  la migration.
- **Aucun mécanisme de backup/restore DB** avant déploiement — voir
  `03-risques-infra.md`.

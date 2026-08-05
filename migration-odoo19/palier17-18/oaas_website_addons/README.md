# oaas_website_addons

Module website pour O.A.A.S. (oaas.fr), Odoo 16.0.

Regroupe trois fonctionnalités :

1. **Import d'articles de blog** depuis un fichier Excel (bilingue EN/FR).
2. **Snippet builder** `s_oaas_tech` — carrousel de logos de technologies.
3. **Fichiers `llms.txt`** — exposition du contenu du site pour les agents IA
   (convention [llmstxt.org](https://llmstxt.org/)).

## Import d'articles de blog

`models/models.py` — `BlogPostImport` (`blog.post.import`) est un assistant
(`TransientModel`). L'utilisateur téléverse un `.xlsx` via le backend ;
`import_data()` :

1. ouvre le classeur avec `openpyxl`, lit la feuille **`Blog import`** ;
2. délègue le parsing par ligne à
   `scripts/test_import_xls.py::convert_row_to_blog_post()` ;
3. crée l'article en `en_US`, puis écrit la version FR via
   `.with_context(lang='fr_FR')` ;
4. le `content` bilingue est stocké en JSON `{"en_US": ..., "fr_FR": ...}` par
   un `UPDATE` SQL direct (contourne la couche de traduction de l'ORM).

Les traductions FR ne sont **pas** auto-générées : chaque champ traduisible a
une colonne FR dédiée juste après sa colonne EN dans l'Excel. Une cellule FR
vide laisse le champ vide.

### Disposition des colonnes (feuille « Blog import », 0-indexé)

| Col | Champ |
|---|---|
| 0 | Nom du blog (lookup) |
| 1 / 2 | Titre — EN / **FR** |
| 3 / 4 | Sous-titre — EN / **FR** |
| 5 | Nom du site (lookup) |
| 6 | Email auteur (lookup) |
| 7 | Date (`dd/mm/yyyy HH:MM:SS`) |
| 8 / 9 | `website_meta_title` — EN / **FR** |
| 10 / 11 | `website_meta_description` — EN / **FR** |
| 12 / 13 | `website_meta_keywords` — EN / **FR** |
| 14 | `is_published` (bool Python) |
| 15 | `active` (bool Python) |
| 16–23 | Why / How / What / Conclusion — EN / **FR** |
| 24–28 | Images Cover / Why / How / What / Conclusion (intégrées) |
| 29 / 30 | Résumé / intro — EN / **FR** |
| 31 / 32 | Accordéon avantages (HTML brut) — EN / **FR** |
| 33 | `to_import` (bool Python) |

Les images sont repérées par leur ancre ligne/colonne dans `sheet._images`,
sauvegardées en `ir.attachment`, et leur URL est injectée dans le HTML.
L'image de couverture (col 24) est stockée dans `cover_properties` du
`blog.post`.

### Générateur de données d'exemple

`scripts/make_sample_xlsx.py` régénère
`scripts/OAAS_BLOG_POST_IOTPlatform.xlsx`. Les contenus (EN + FR) vivent dans
`scripts/sample_articles_data.py`. Lancer `python make_sample_xlsx.py` depuis
`scripts/`. Les colonnes images sont laissées vides (re-coller les images dans
le xlsx ensuite).

## Snippet website `s_oaas_tech`

`views/templates.xml` définit `s_oaas_tech`, une section pleine largeur de
carrousel de logos, injectée dans la palette du builder via
`external_snippets_add` (hérite `website.snippets`). L'override
`brand_promotion` retire la barre de branding Odoo en pied de page.

## Fichiers llms.txt

- `models/oaas_llms_builder.py` — `oaas.llms.builder` : génère le contenu
  `llms.txt` / `llms-full.txt` depuis les articles de blog publiés.
- `models/res_config_settings.py` — mode (auto/manuel), en-tête, contenu manuel,
  configurables dans **Paramètres → Site Web**.
- `controllers/controllers.py` — sert `/llms.txt` et `/llms-full.txt` à la
  racine du site.

## Dépendances

- Odoo : `web`, `web_editor`, `http_routing`, `portal`, `website_blog`
- Python : `openpyxl`, `Pillow`

## Mise à jour

```bash
odoo -u oaas_website_addons --stop-after-init   # recharge modèles/XML
```

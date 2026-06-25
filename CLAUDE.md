# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Custom Odoo 16.0 addons for O.A.A.S. (oaas.fr). Two modules live in this repo:

- **`oaas_website_addons`** — active website module: blog post bulk import from Excel (bilingual EN/FR), a custom website builder snippet (`s_oaas_tech`) showing a technology carousel, and CSS overrides for the slideshow template.
- **`oaas_docusign_addons`** — scaffolded module for DocuSign integration (not yet implemented).

## Server environment

| Item | Value |
|---|---|
| Odoo install | `/var/www/html/odoo/` |
| Config file | `/var/www/html/odoo/odoo.conf` |
| Addons path | `/var/www/html/odoo/odoo-oaas-addons,/var/www/html/odoo/addons` |
| Log file | `/var/www/html/odoo/log/odoo-server.log` |
| DB | PostgreSQL `oaas` on `localhost:5432`, user `odoo` |
| Systemd service | `odoo.service` |

## Common commands

```bash
# Restart the Odoo service (required after any Python/XML change)
sudo systemctl restart odoo

# Tail the log
tail -f /var/www/html/odoo/log/odoo-server.log

# Update a specific module (forces XML/model reload without full restart)
/var/www/html/odoo/.venv/bin/python3 /var/www/html/odoo/odoo-bin \
  --config=/var/www/html/odoo/odoo.conf \
  -u oaas_website_addons --stop-after-init

# Install Python deps into the Odoo venv
/var/www/html/odoo/.venv/bin/pip install openpyxl pillow

# Run the standalone XLS import test script (outside Odoo, direct DB)
/var/www/html/odoo/.venv/bin/python3 \
  /var/www/html/odoo/odoo-oaas-addons/oaas_website_addons/scripts/test_import_xls.py
```

## Architecture: `oaas_website_addons`

### Blog post import flow

`models/models.py` — `BlogPostImport` (`blog.post.import`) is a `TransientModel` (wizard). The user uploads an `.xlsx` file via the backend form. `import_data()`:

1. Decodes the binary, opens it with `openpyxl`, reads the sheet named **`Blog import`**.
2. Delegates per-row parsing to `scripts/test_import_xls.py::convert_row_to_blog_post()`, which maps fixed column positions to `blog.post` fields and assembles raw Odoo website builder HTML for the content.
3. Creates the post in `en_US`, then writes the French version via `.with_context(lang='fr_FR')`.
4. Bilingual `content` is stored as a JSON string `{"en_US": "...", "fr_FR": "..."}` written directly via a raw SQL `UPDATE` (bypassing the ORM translation layer).

French text is **no longer auto-translated**: every translated field has a dedicated FR column right after its EN column in the Excel file (translations are produced upstream, e.g. by AI inside the xlsx). An empty FR cell leaves that field empty — there is no API fallback.

### Excel column layout (sheet "Blog import", 0-indexed)

| Col | Field |
|---|---|
| 0 | Blog name (lookup) |
| 1 / 2 | Post title — EN / **FR** |
| 3 / 4 | Subtitle — EN / **FR** |
| 5 | Website name (lookup) |
| 6 | Author email (lookup) |
| 7 | Post date (`dd/mm/yyyy HH:MM:SS`) |
| 8 / 9 | `website_meta_title` — EN / **FR** |
| 10 / 11 | `website_meta_description` — EN / **FR** |
| 12 / 13 | `website_meta_keywords` — EN / **FR** |
| 14 | `is_published` (Python bool string) |
| 15 | `active` (Python bool string) |
| 16 / 17 | Why text — EN / **FR** |
| 18 / 19 | How text — EN / **FR** |
| 20 / 21 | What text — EN / **FR** |
| 22 / 23 | Conclusion text — EN / **FR** |
| 24–28 | Cover / Why / How / What / Conclusion images (embedded) |
| 29 / 30 | Summary / intro — EN / **FR** |
| 31 / 32 | Advantages accordion (raw HTML) — EN / **FR** |
| 33 | `to_import` flag (Python bool string, e.g. `True`) |

The SEO/meta fields are translatable in Odoo: the EN value goes on the post created in `en_US`, then the FR value is written in the `fr_FR` context alongside `name`/`subtitle`. Images are matched by their anchor row/col in `sheet._images` (cols 24–28). Each image is saved as an `ir.attachment` and its URL is embedded in the HTML content.

### Sample data generator

`scripts/make_sample_xlsx.py` regenerates `scripts/OAAS_BLOG_POST_IOTPlatform.xlsx` (a sample import file in the 31-column format). The article contents (EN + FR, one dict per post) live in `scripts/sample_articles_data.py`; the accordion is factored through `_advantages()` / `_advantages_fr()` since only the first item's label changes per article. Image columns are left empty (re-paste images in the xlsx afterwards). Run `python make_sample_xlsx.py` from the `scripts/` dir.

### Website snippet

`views/templates.xml` defines `s_oaas_tech` — a full-width technology logo carousel section injected into the website builder's snippet palette via `external_snippets_add` (inherits `website.snippets`). The `brand_promotion` template override removes the Odoo branding footer bar.

## Key dependencies

- `openpyxl` — Excel read/write
- `Pillow` (PIL) — image handling in import script

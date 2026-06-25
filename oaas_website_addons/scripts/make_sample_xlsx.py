# -*- coding: utf-8 -*-
"""
Genere un fichier .xlsx compatible avec l'import blog.post.import
(feuille "Blog import", 31 colonnes 0-indexees).

Reprend les articles du blog OAAS (cf. OAAS_BLOG_POSTs_migrated). Le contenu est
fourni dans les DEUX langues : chaque champ traduit a une colonne EN suivie
immediatement de sa colonne FR. Le pipeline d'import ne traduit plus rien (plus
de dependance a une API) : il lit directement la colonne FR. Une cellule FR vide
laisse le champ correspondant vide cote francais.

Les colonnes image (cover/why/how/what/conclusion) sont laissees vides : les
images embarquees sont recollees dans le xlsx ensuite. to_import vaut True
partout (tous les articles seront importes).

Les donnees des articles vivent dans sample_articles_data.py.

Usage :
    python make_sample_xlsx.py
    -> ecrit OAAS_BLOG_POST_IOTPlatform.xlsx a cote du script
"""
import os
import openpyxl

try:
    # Execution directe : python make_sample_xlsx.py
    from sample_articles_data import ARTICLES, AUTHOR_EMAIL, WEBSITE, _advantages, _advantages_fr
except ImportError:
    # Import en tant que module du package.
    from .sample_articles_data import ARTICLES, AUTHOR_EMAIL, WEBSITE, _advantages, _advantages_fr


# --- En-tetes (ligne 0, ignoree a l'import) --------------------------------
HEADERS = [
    "Blog",                    # 0  blog.blog name (lookup)
    "Title (EN)",              # 1  name (EN)
    "Title (FR)",              # 2  name (FR)
    "Subtitle (EN)",           # 3  subtitle (EN)
    "Subtitle (FR)",           # 4  subtitle (FR)
    "Website",                 # 5  website name (lookup)
    "Author email",            # 6  res.users email (lookup)
    "Post date",               # 7  dd/mm/yyyy HH:MM:SS
    "Meta title (EN)",         # 8
    "Meta title (FR)",         # 9
    "Meta description (EN)",   # 10
    "Meta description (FR)",   # 11
    "Meta keywords (EN)",      # 12
    "Meta keywords (FR)",      # 13
    "is_published",            # 14 bool str
    "active",                  # 15 bool str
    "Why text (EN)",           # 16
    "Why text (FR)",           # 17
    "How text (EN)",           # 18
    "How text (FR)",           # 19
    "What text (EN)",          # 20
    "What text (FR)",          # 21
    "Conclusion text (EN)",    # 22
    "Conclusion text (FR)",    # 23
    "Cover image",             # 24 (image anchor)
    "Why image",               # 25 (image anchor)
    "How image",               # 26 (image anchor)
    "What image",              # 27 (image anchor)
    "Conclusion image",        # 28 (image anchor)
    "Summary (EN)",            # 29 resume / intro (EN)
    "Summary (FR)",            # 30 resume / intro (FR)
    "Advantages HTML (EN)",    # 31 accordeon optionnel : HTML brut colle du builder
    "Advantages HTML (FR)",    # 32
    "to_import",               # 33 bool str
]


def _row(article):
    # Construit la ligne (34 colonnes) pour un article. Les images (24-28) sont
    # vides (recollees ensuite) ; is_published = True et to_import = True.
    return [
        article["blog"],                                  # 0
        article["title"],                                 # 1
        article["title_fr"],                              # 2
        article["subtitle"],                              # 3
        article["subtitle_fr"],                           # 4
        WEBSITE,                                          # 5
        AUTHOR_EMAIL,                                     # 6
        article["post_date"],                             # 7
        article["meta_title"],                            # 8
        article["meta_title_fr"],                         # 9
        article["meta_description"],                      # 10
        article["meta_description_fr"],                   # 11
        article["meta_keywords"],                         # 12
        article["meta_keywords_fr"],                      # 13
        "True",                                           # 14 is_published
        "True",                                           # 15 active
        article["why"],                                   # 16
        article["why_fr"],                                # 17
        article["how"],                                   # 18
        article["how_fr"],                                # 19
        article["what"],                                  # 20
        article["what_fr"],                               # 21
        article["conclusion"],                            # 22
        article["conclusion_fr"],                         # 23
        "", "", "", "", "",                               # 24-28 images (vides)
        article["summary"],                               # 29
        article["summary_fr"],                            # 30
        _advantages(article["adv_label"]),                # 31
        _advantages_fr(article["adv_label_fr"]),          # 32
        "True",                                            # 33 to_import
    ]


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Blog import"
    ws.append(HEADERS)
    for article in ARTICLES:
        ws.append(_row(article))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "OAAS_BLOG_POST_IOTPlatform.xlsx")
    wb.save(out)
    print("Ecrit :", out, "-", len(ARTICLES), "articles")


if __name__ == "__main__":
    main()

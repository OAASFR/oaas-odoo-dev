# Image Odoo 16 officielle + dépendances Python des addons OAAS
FROM odoo:16.0

# Les pip install nécessitent root
USER root

# Dépendances Python additionnelles (cf. external_dependencies des addons)
# requests : appels à l'API LinkedIn (oaas_linkedin_addons)
RUN pip3 install --no-cache-dir openpyxl translate nltk pillow requests \
    # Tokenizer NLTK requis par l'import de blog (sentence splitting)
    && python3 -c "import nltk; nltk.download('punkt', download_dir='/usr/share/nltk_data')" \
    && python3 -c "import nltk; nltk.download('punkt_tab', download_dir='/usr/share/nltk_data')" || true

# NLTK cherche ses données dans ce chemin (lisible par l'utilisateur odoo)
ENV NLTK_DATA=/usr/share/nltk_data

# Retour à l'utilisateur odoo non-privilégié (défaut de l'image)
USER odoo

# -*- coding: utf-8 -*-
"""Migration addon post-migrate — palier 16.0 -> 17.0.0.1.0.

Squelette au format standard Odoo (odoo/tools/convert.py::MigrationManager),
exécuté automatiquement par `-u oaas_linkedin_addons` sur un Odoo 17 si un
fichier `migrations/<version>/post-migrate.py` existe pour cette version.

Aucune transformation de donnée n'est nécessaire à ce palier : l'inventaire
(migration-odoo19/01-inventaire-technique.md) n'identifie aucun renommage de
champ/modèle propre à ce module entre 16.0 et 17.0. Les seuls changements
sont côté vues (attrs= -> invisible=), sans impact sur les données stockées
(tokens LinkedIn, config IA en ir.config_parameter, inchangés).
Ce fichier reste en place, prêt si un besoin de transformation de données
est identifié plus tard sur ce palier.
"""


def migrate(cr, version):
    pass

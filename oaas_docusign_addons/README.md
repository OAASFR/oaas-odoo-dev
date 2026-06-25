# oaas_docusign_addons

Module Odoo 16.0 pour O.A.A.S. (oaas.fr) destiné à l'intégration **DocuSign**.

> ⚠️ **Statut : scaffold (non implémenté).**
> Le module est généré par `odoo scaffold` ; les modèles, vues et contrôleurs
> sont encore vides ou commentés. Il ne fournit aucune fonctionnalité à ce jour.

## État actuel

| Élément | État |
|---|---|
| `models/models.py` | Vide (exemple commenté) |
| `controllers/controllers.py` | Vide (exemple commenté) |
| `views/views.xml`, `views/templates.xml` | Gabarits scaffold |
| `__manifest__.py` | Métadonnées par défaut (`depends: ['base']`) |

## Travail restant (indicatif)

- Définir les modèles (configuration des identifiants DocuSign, suivi des
  enveloppes).
- Implémenter l'authentification (OAuth / JWT DocuSign).
- Contrôleurs pour les webhooks de statut (DocuSign Connect).
- Vues backend + sécurité (`ir.model.access.csv`).
- Renseigner `author`, `website`, `summary`, `license` dans le manifest.

## Dépendances

- Odoo : `base`

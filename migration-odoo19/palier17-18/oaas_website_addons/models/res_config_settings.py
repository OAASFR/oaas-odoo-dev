# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Mode de génération du contenu llms.txt / llms-full.txt.
    #   auto   -> contenu regénéré dynamiquement depuis les blog.post publiés
    #   manual -> contenu servi tel quel depuis les champs ci-dessous
    oaas_llms_mode = fields.Selection(
        selection=[
            ('auto', _('Automatique (depuis les articles de blog)')),
            ('manual', _('Manuel (contenu personnalisé)')),
        ],
        string=_('Mode de génération llms.txt'),
        default='auto',
        config_parameter='oaas_website_addons.llms_mode',
    )
    # Lignes d'en-tête optionnelles ajoutées en haut des deux fichiers
    # (par ex. titre du site, description, contact). Utilisé en mode auto ET
    # manuel comme préambule.
    # NB : res.config.settings n'accepte pas les champs Text liés à un
    # config_parameter (default_get / _get_classified_fields refuse tout type
    # autre que char/bool/int/float/selection/m2o/datetime). On utilise donc
    # Char + widget="text" dans la vue pour conserver une saisie multi-ligne.
    oaas_llms_header = fields.Char(
        string=_('En-tête llms.txt'),
        config_parameter='oaas_website_addons.llms_header',
    )
    # Contenu servi tel quel quand oaas_llms_mode == 'manual'.
    oaas_llms_txt = fields.Char(
        string=_('Contenu llms.txt'),
        config_parameter='oaas_website_addons.llms_txt',
    )
    oaas_llms_full_txt = fields.Char(
        string=_('Contenu llms-full.txt'),
        config_parameter='oaas_website_addons.llms_full_txt',
    )

    def action_oaas_generate_llms(self):
        """Pré-remplit les champs manuels avec le rendu auto courant.

        Permet à l'utilisateur de partir de la génération automatique puis de
        l'éditer à la main (mode "auto + override manuel").
        """
        self.ensure_one()
        website = self.env['website'].get_current_website()
        Builder = self.env['oaas.llms.builder']
        self.oaas_llms_txt = Builder.build_llms_txt(website, full=False)
        self.oaas_llms_full_txt = Builder.build_llms_txt(website, full=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

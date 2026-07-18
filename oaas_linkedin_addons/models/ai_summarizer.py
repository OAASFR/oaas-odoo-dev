# -*- coding: utf-8 -*-
"""Génération du texte d'un post LinkedIn via un modèle compatible API
OpenAI (ex. Ollama exposant /v1/chat/completions).

Ne génère jamais l'URL de l'article : le lien est ajouté par l'appelant
(blog_post.py) après coup, pour éviter toute hallucination d'URL par le
modèle. Centralise les accès ir.config_parameter en sudo(), comme
linkedin_client.py.
"""
import logging
import re

import requests

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Valeurs de repli si Paramètres → Site Web → LinkedIn → « Résumé IA » est
# vide (endpoint Ollama de validation, modèle léger suffisant pour un résumé).
# qwen2.5-coder:3b et non un modèle qwen3 : les modèles qwen3 de ce serveur
# tournent en mode "réflexion" (thinking) et ni reasoning_effort=none ni
# /no_think ne le désactivent sur cette version d'Ollama — le raisonnement
# consomme tout le budget de tokens sans jamais produire de réponse finale
# (testé jusqu'à 3000 tokens / 11 min en streaming, toujours tronqué).
DEFAULT_AI_BASE_URL = 'https://ollama.validation.oaas.fr/v1'
DEFAULT_AI_MODEL = 'qwen2.5-coder:3b'
# 0.0 (déterministe) : un petit modèle comme qwen2.5-coder:3b s'écarte plus
# facilement du contenu source et des consignes de format à température
# élevée (testé : hallucinations hors-sujet à 0.7). Repli conservateur.
DEFAULT_AI_TEMPERATURE = 0.0
DEFAULT_AI_MAX_TOKENS = 700
DEFAULT_AI_TIMEOUT = 60

# Timeout court dédié au listing des modèles (simple sondage, pas une
# génération) : indépendant du timeout configurable de generate_commentary.
LIST_MODELS_TIMEOUT = 10

SYSTEM_PROMPT = (
    "Tu rédiges des posts LinkedIn B2B en {lang} pour une entreprise de "
    "conseil en systèmes d'information. À partir du titre, du sous-titre et "
    "du contenu d'un article de blog, produis UNIQUEMENT le texte du post, "
    "structuré ainsi :\n"
    "1. Une accroche percutante (contrariante ou chiffrée), 200 caractères "
    "maximum, sur sa propre ligne.\n"
    "2. Un saut de ligne, puis 2 à 4 puces courtes et concrètes reprenant "
    "les enseignements clés de l'article (utilise le tiret '-').\n"
    "3. Un saut de ligne, puis une phrase d'appel à l'action invitant à "
    "lire l'article complet, SANS insérer d'URL : elle sera ajoutée "
    "automatiquement après ton texte.\n"
    "4. Une dernière ligne avec 3 à 5 hashtags pertinents.\n"
    "Longueur totale visée : 1300 à 1900 caractères. Ton direct, expert, "
    "jamais commercial ni ronflant. N'utilise JAMAIS les mots « Voici » ou "
    "« Découvrez », même en début de section. Ne mentionne jamais que tu es "
    "une IA. N'ajoute AUCUN label ou intitulé avant une section (interdits : "
    "« Accroche : », « Accroche percutante : », « Appel à l'action : », "
    "« Hashtags : » ou équivalent) : seulement le texte brut du post, "
    "prêt à être publié tel quel. Réponds uniquement avec ce texte, sans "
    "balises ni commentaire."
)

# Exemple few-shot (entrée/sortie fictives, sans rapport avec le contenu réel
# du client) : les petits modèles suivent nettement mieux le format et
# restent sur le sujet de l'article quand un exemple concret accompagne les
# instructions plutôt qu'une simple description textuelle du format.
FEW_SHOT_USER = (
    "Titre : Sauvegardes chiffrées : le contrôle qui évite le pire\n"
    "Sous-titre : Ce qui distingue une sauvegarde qui protège vraiment "
    "d'une sauvegarde qui rassure à tort\n\n"
    "Contenu de l'article :\n"
    "Beaucoup d'entreprises sauvegardent leurs données sans jamais tester "
    "la restauration. Résultat : la sauvegarde existe, mais personne ne "
    "sait si elle fonctionne réellement le jour où il le faut.\n\n"
    "Trois pratiques changent la donne : chiffrer les sauvegardes au repos "
    "et en transit, les stocker sur un site distinct de la production, et "
    "tester une restauration complète au moins une fois par trimestre. "
    "Sans ce test régulier, une sauvegarde corrompue ou incomplète n'est "
    "détectée qu'au pire moment.\n\n"
    "Mettre en place ces trois pratiques ne demande ni gros budget ni "
    "refonte d'infrastructure : surtout une procédure claire et un "
    "responsable identifié pour l'exécuter."
)
FEW_SHOT_ASSISTANT = (
    "90% des sauvegardes ne sont jamais testées. Le jour où elles servent, "
    "il est trop tard pour le découvrir.\n\n"
    "- Une sauvegarde non restaurée n'est qu'une hypothèse, pas une "
    "protection\n"
    "- Le chiffrement au repos et en transit ferme une faille souvent "
    "ignorée\n"
    "- Un site de stockage distinct de la production évite la perte totale\n"
    "- Un test de restauration trimestriel révèle les corruptions avant "
    "qu'elles coûtent cher\n\n"
    "L'article détaille la procédure à mettre en place, sans budget "
    "supplémentaire ni refonte d'infrastructure.\n\n"
    "#Cybersécurité #SauvegardeDonnées #ContinuitéActivité #InfrastructureIT"
)

# Certains modèles (dont Qwen3) peuvent renvoyer un bloc de raisonnement
# <think>...</think> avant la réponse finale selon le template de chat utilisé
# côté serveur d'inférence ; on le retire par sécurité s'il est présent.
_THINK_BLOCK_RE = re.compile(r'<think>.*?</think>', re.DOTALL)


class LinkedInAiSummarizer(models.AbstractModel):
    _name = 'oaas.linkedin.ai_summarizer'
    _description = "Génération du texte de post LinkedIn via IA"

    def _get_param(self, key):
        return self.env['ir.config_parameter'].sudo().get_param(
            'oaas_linkedin.%s' % key)

    def _base_url(self):
        return (self._get_param('ai_base_url') or DEFAULT_AI_BASE_URL).rstrip('/')

    def _model(self):
        return self._get_param('ai_model') or DEFAULT_AI_MODEL

    def _temperature(self):
        try:
            return float(self._get_param('ai_temperature') or DEFAULT_AI_TEMPERATURE)
        except ValueError:
            return DEFAULT_AI_TEMPERATURE

    def _max_tokens(self):
        try:
            return int(self._get_param('ai_max_tokens') or DEFAULT_AI_MAX_TOKENS)
        except ValueError:
            return DEFAULT_AI_MAX_TOKENS

    def _timeout(self):
        try:
            return int(self._get_param('ai_timeout') or DEFAULT_AI_TIMEOUT)
        except ValueError:
            return DEFAULT_AI_TIMEOUT

    def _headers(self, api_key=None):
        headers = {'Content-Type': 'application/json'}
        key = api_key if api_key is not None else self._get_param('ai_api_key')
        if key:
            headers['Authorization'] = 'Bearer %s' % key
        return headers

    def list_models(self, base_url=None, api_key=None):
        """Interroge {base_url}/models et retourne les identifiants de modèle
        disponibles, triés. base_url/api_key permettent de sonder des valeurs
        pas encore enregistrées (formulaire de config en cours d'édition) ;
        sinon repli sur la configuration stockée. Lève UserError si l'appel
        échoue."""
        url = (base_url or self._base_url()).rstrip('/')
        try:
            resp = requests.get(
                '%s/models' % url,
                headers=self._headers(api_key=api_key),
                timeout=LIST_MODELS_TIMEOUT)
            resp.raise_for_status()
            data = resp.json().get('data', [])
            return sorted(item['id'] for item in data if item.get('id'))
        except (requests.RequestException, ValueError, KeyError, TypeError) as e:
            raise UserError(_("Impossible de lister les modèles IA : %s") % e)

    def generate_commentary(self, title, subtitle, plain_text, lang):
        """Retourne le texte du post (accroche + puces + CTA + hashtags),
        sans lien. Lève UserError si l'appel échoue ou renvoie un texte vide.
        """
        lang_label = 'français' if (lang or '').startswith('fr') else 'anglais'
        user_content = "Titre : %s\nSous-titre : %s\n\nContenu de l'article :\n%s" % (
            title or '', subtitle or '', plain_text or '')

        payload = {
            'model': self._model(),
            'messages': [
                {'role': 'system',
                 'content': SYSTEM_PROMPT.format(lang=lang_label)},
                {'role': 'user', 'content': FEW_SHOT_USER},
                {'role': 'assistant', 'content': FEW_SHOT_ASSISTANT},
                {'role': 'user', 'content': user_content},
            ],
            'temperature': self._temperature(),
            'max_tokens': self._max_tokens(),
            'stream': False,
            # Sans ça, les modèles "thinking" (dont Qwen3) peuvent épuiser
            # max_tokens entièrement dans le raisonnement interne (champ
            # "reasoning" de la réponse) et renvoyer un content vide avec
            # finish_reason=length. Cette tâche est un résumé simple, aucun
            # besoin de chaîne de raisonnement.
            'reasoning_effort': 'none',
        }
        try:
            resp = requests.post(
                '%s/chat/completions' % self._base_url(),
                headers=self._headers(),
                json=payload,
                timeout=self._timeout())
            resp.raise_for_status()
            commentary = resp.json()['choices'][0]['message']['content']
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            _logger.warning("LinkedIn AI summarizer failed: %s", e)
            raise UserError(_(
                "Échec de la génération IA du résumé LinkedIn : %s") % e)

        commentary = _THINK_BLOCK_RE.sub('', commentary).strip()
        if not commentary:
            raise UserError(_(
                "Le modèle IA a renvoyé un résumé vide pour le post LinkedIn."))
        return commentary

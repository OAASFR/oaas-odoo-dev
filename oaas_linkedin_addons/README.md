# oaas_linkedin_addons

Publie les articles de blog Odoo sur la **page entreprise LinkedIn**, à la demande.

Module Odoo 16.0 pour O.A.A.S. (oaas.fr).

## Fonctionnalités

- Action **« Publier sur LinkedIn »** sur les articles de blog :
  - bouton (smart button) sur le formulaire de l'article,
  - entrée dans le menu **Action ⚙️** des vues liste et formulaire (publication multiple).
- Contenu publié : **titre + sous-titre + lien** vers l'article, et **image de couverture** uploadée comme média (repli sur une carte article si l'article n'a pas de couverture).
- **Idempotence** : un article déjà publié (porteur d'un `linkedin_post_urn`) n'est jamais republié. Un bouton « Republier » apparaît uniquement après une erreur.
- Configuration et connexion OAuth dans **Paramètres → Site Web → LinkedIn**.

> ⚠️ Il n'y a **pas** de publication automatique : rien n'est posté tant qu'un utilisateur ne déclenche pas l'action.

## Prérequis LinkedIn (bloquant)

La publication au nom d'une page entreprise nécessite, côté
[LinkedIn Developer Platform](https://developer.linkedin.com) :

1. Une **app** liée à la page entreprise.
2. Le produit **Community Management API** ajouté à l'app (revue manuelle par LinkedIn).
3. Les scopes OAuth : `w_organization_social`, `r_organization_social`, `rw_organization_admin`.
4. L'**Organization URN** de la page (`urn:li:organization:123456`).
5. Le **redirect URI** déclaré dans l'app, exactement égal à
   `<web.base.url>/linkedin/oauth/callback`
   (ex. `https://oaas.fr/linkedin/oauth/callback`, ou
   `http://localhost:8069/linkedin/oauth/callback` en local).

> LinkedIn ne fournit pas de sandbox. Pour tester : utiliser une app en tier
> *Development* avec son propre compte admin, et/ou publier sur une page de test.

## Configuration

**Paramètres → Site Web → section LinkedIn** :

| Champ | Description |
|---|---|
| Client ID | Client ID de l'app LinkedIn |
| Client Secret | Client Secret de l'app |
| Organization URN | `urn:li:organization:<id>` de la page |
| Bouton « Connecter LinkedIn » | Lance le flux OAuth, stocke le jeton |

Le **jeton d'accès** (et son refresh) est obtenu par OAuth, stocké en
`ir.config_parameter` (clés `oaas_linkedin.access_token` /
`refresh_token` / `token_expiry`) et **jamais exposé** dans l'interface. Il est
rafraîchi automatiquement avant expiration.

## Utilisation

1. Renseigner la configuration ci-dessus, cliquer **Connecter LinkedIn**, autoriser l'app.
2. Ouvrir un article de blog → **Publier sur LinkedIn** (smart button),
   ou sélectionner plusieurs articles en liste → **Action ⚙️ → Publier sur LinkedIn**.
3. Le statut (`Non publié` / `Publié` / `Erreur`) et l'éventuel message d'erreur
   sont visibles dans le groupe *Options de publication* de l'article.

## Architecture

| Fichier | Rôle |
|---|---|
| `models/linkedin_client.py` | `AbstractModel` `oaas.linkedin.client` : OAuth (autorisation, échange de code, refresh), upload d'image en deux temps, création du post (`POST /rest/posts`). Centralise les accès `ir.config_parameter` en `sudo()`. |
| `models/res_config_settings.py` | Champs de config (Client ID/Secret/Org URN) + bouton de connexion. |
| `models/blog_post.py` | Hérite `blog.post` : champs `linkedin_post_urn` / `linkedin_state` / `linkedin_error`, méthode `action_publish_to_linkedin()` (idempotente, agrège un résumé). |
| `controllers/linkedin_oauth.py` | Routes `/linkedin/oauth/connect` et `/linkedin/oauth/callback` (state anti-CSRF). |
| `data/ir_actions_server.xml` | Action serveur liée à `blog.post` (menu Action ⚙️). |
| `views/res_config_settings_views.xml` | Bloc LinkedIn dans les paramètres du site. |
| `views/blog_post_views.xml` | Smart button + statut sur le formulaire d'article. |

La version de l'API LinkedIn est figée dans `LINKEDIN_API_VERSION`
(`models/linkedin_client.py`) — à mettre à jour si l'API renvoie une erreur de
version.

## Dépendances

- Odoo : `website_blog`
- Python : `requests`

## Installation

```bash
# Mettre à jour la liste des modules puis installer
odoo -d <db> -i oaas_linkedin_addons --stop-after-init
# puis redémarrer le service
```

Ou via l'interface : **Applications → Mettre à jour la liste des applications → Installer**.

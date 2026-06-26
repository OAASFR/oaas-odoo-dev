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

1. Une **page entreprise** LinkedIn dont vous êtes administrateur.
2. Une **app** LinkedIn liée à cette page.
3. Le produit **Community Management API** ajouté à l'app (revue manuelle par LinkedIn).
4. Les scopes OAuth : `w_organization_social`, `r_organization_social`, `rw_organization_admin`.
5. Le **Client ID**, le **Client Secret**, l'**Organization URN**
   (`urn:li:organization:123456`) et le **redirect URI** à renseigner dans Odoo.

> LinkedIn ne fournit pas de sandbox. Pour tester : utiliser une app en tier
> *Development* avec son propre compte admin, et/ou publier sur une page de test.

## Tutoriel : configurer l'app LinkedIn pas à pas

### Étape 1 — Créer (ou récupérer) la page entreprise

La publication se fait **au nom d'une page entreprise**, pas d'un profil personnel.
Il faut donc une page existante dont vous êtes **administrateur**.

1. Si vous n'en avez pas : [linkedin.com/company/setup/new](https://www.linkedin.com/company/setup/new)
   → choisir « Page entreprise », renseigner nom, secteur, logo, puis **Créer la page**.
2. Vérifiez votre rôle : page → **Outils d'admin → Gérer les administrateurs**.
   Vous devez y figurer comme **Super administrateur**.
3. Notez l'**identifiant numérique** de la page (utile pour l'Organization URN — voir étape 5) :
   il apparaît dans l'URL de l'admin de la page, par ex.
   `https://www.linkedin.com/company/`**`123456`**`/admin/`.

### Étape 2 — Créer l'app LinkedIn

1. Aller sur [linkedin.com/developers/apps](https://www.linkedin.com/developers/apps)
   → **Create app**.
2. Renseigner :
   - **App name** : un nom (ex. `OAAS Odoo Publisher`).
   - **LinkedIn Page** : **la page entreprise de l'étape 1** (ce lien est
     obligatoire et conditionne l'accès aux produits *organization*).
   - **App logo** : un logo (obligatoire).
   - Cocher l'accord d'utilisation, puis **Create app**.
3. Onglet **Settings** → **Verify** : générer le lien de vérification et le
   valider depuis le compte admin de la page (associe définitivement l'app à la page).

### Étape 3 — Ajouter les bons produits

Onglet **Products** de l'app :

1. **Sign In with LinkedIn using OpenID Connect** — ajout immédiat, fournit le
   socle OAuth.
2. **Community Management API** — **requis** pour publier au nom de la page.
   Cliquer **Request access**, remplir le formulaire (cas d'usage : publication
   d'articles de blog sur la page entreprise). ⚠️ Cet accès est soumis à une
   **revue manuelle de LinkedIn** (de quelques heures à plusieurs jours). Tant
   qu'il n'est pas accordé, la création de post échoue.

> En attendant la validation, vous pouvez déjà finir la configuration et tester
> le flux OAuth ; seule la publication restera bloquée.

### Étape 4 — Déclarer le redirect URI et relever les scopes

1. Onglet **Auth** → section **OAuth 2.0 settings** → **Authorized redirect URLs
   for your app** → ajouter **exactement** :

   ```
   <web.base.url>/linkedin/oauth/callback
   ```

   où `<web.base.url>` est l'URL de votre Odoo (paramètre système `web.base.url`) :
   - production : `https://oaas.fr/linkedin/oauth/callback`
   - local : `http://localhost:8069/linkedin/oauth/callback`

   La moindre différence (slash final, http/https, port) fait échouer le callback.

2. Onglet **Auth** → **OAuth 2.0 scopes** : vérifier que les scopes suivants
   sont disponibles (ils apparaissent une fois la *Community Management API*
   accordée) :
   `w_organization_social`, `r_organization_social`, `rw_organization_admin`.
   Le module les demande automatiquement lors de la connexion.

### Étape 5 — Relever les identifiants à saisir dans Odoo

| À récupérer | Où le trouver |
|---|---|
| **Client ID** | App → onglet **Auth** → *Application credentials* → `Client ID` |
| **Client Secret** | App → onglet **Auth** → *Application credentials* → `Client Secret` (bouton afficher/copier) |
| **Organization URN** | `urn:li:organization:<id>` où `<id>` est l'identifiant numérique de la page (étape 1.3), ex. `urn:li:organization:123456` |

Puis passer à la section **Configuration** ci-dessous.

## Configuration

**Paramètres → Site Web → section LinkedIn** (valeurs relevées au *Tutoriel*
ci-dessus) :

| Champ | Description |
|---|---|
| Client ID | Client ID de l'app LinkedIn (étape 5) |
| Client Secret | Client Secret de l'app (étape 5) |
| Organization URN | `urn:li:organization:<id>` de la page (étape 5) |
| Publier en brouillon (non diffusé) | Crée le post en `DRAFT` (présent sur la page mais non diffusé) — pour tester sans publier réellement |
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

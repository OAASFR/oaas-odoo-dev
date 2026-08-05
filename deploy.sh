#!/bin/bash
set -euo pipefail

ODOO_DIR="/var/www/html/odoo"
ODOO_BRANCH="16.0"
ODOO_BIN="/usr/local/bin/odoo"
SERVICE_FILE="/etc/systemd/system/odoo.service"
# Même valeur écrite dans odoo.conf plus bas (réutilisée pour la restauration
# de base) — secret en clair, dette connue, voir migration-odoo19/03-risques-infra.md
ODOO_DB_PASSWORD="Maison63#123"

echo "=== Mot de passe sudo (demandé une seule fois) ==="
sudo -v

read -rp "Utilisateur système Odoo [oaas:www-data] : " ODOO_OWNER
ODOO_OWNER="${ODOO_OWNER:-oaas:www-data}"
ODOO_USER="${ODOO_OWNER%%:*}"
ODOO_GROUP="${ODOO_OWNER##*:}"
echo "Permissions : ${ODOO_OWNER}"

read -rp "Domaine du vhost Apache [validation.odoo.oaas.fr] : " APACHE_DOMAIN
APACHE_DOMAIN="${APACHE_DOMAIN:-validation.odoo.oaas.fr}"
echo "Vhost Apache : ${APACHE_DOMAIN}"

read -rp "Email Let's Encrypt pour le certificat SSL [vide = pas de certificat] : " LETSENCRYPT_EMAIL
if [ -n "${LETSENCRYPT_EMAIL}" ]; then
    echo "Certificat SSL : sera demandé pour ${APACHE_DOMAIN} (nécessite que le domaine"
    echo "pointe déjà vers ce serveur et que le port 80 soit joignable depuis internet)."
else
    echo "Aucun email fourni — le vhost restera en HTTP (pas de certificat SSL)."
fi

echo "=== Base de données (zip de sauvegarde production, standard Odoo : dump.sql + filestore/) ==="
read -rp "Chemin du .zip de sauvegarde production [vide = ne pas installer de base] : " PROD_BACKUP_ZIP
read -rp "Nom de la base Odoo cible [oaas_validation] : " ODOO_DB_NAME
ODOO_DB_NAME="${ODOO_DB_NAME:-oaas_validation}"
if [ -n "${PROD_BACKUP_ZIP}" ]; then
    [ -f "${PROD_BACKUP_ZIP}" ] || { echo "Fichier introuvable : ${PROD_BACKUP_ZIP}" >&2; exit 1; }
    for bin in unzip psql createdb dropdb; do
        command -v "$bin" &>/dev/null || { echo "Commande '$bin' introuvable (paquet postgresql-client / unzip requis)" >&2; exit 1; }
    done
    echo "Base cible : ${ODOO_DB_NAME} (restaurée depuis ${PROD_BACKUP_ZIP})"
else
    echo "Aucun zip fourni — l'installation de base sera sautée (étape 7)."
fi

echo "=== Credentials GitHub (Personal Access Token si 2FA activé) ==="
read -rp "GitHub username : " GH_USER
read -rsp "GitHub password / token : " GH_PASS
echo ""
ODOO_REPO="https://${GH_USER}:${GH_PASS}@github.com/odoo/odoo.git"

echo "=== 1. Git pull / clone Odoo ${ODOO_BRANCH} ==="
if [ -d "${ODOO_DIR}/.git" ]; then
    git -C "${ODOO_DIR}" fetch origin
    git -C "${ODOO_DIR}" checkout "${ODOO_BRANCH}"
    git -C "${ODOO_DIR}" pull origin "${ODOO_BRANCH}"
else
    sudo mkdir -p "${ODOO_DIR}"
    sudo chown "$(id -un)" "${ODOO_DIR}"
    git clone --branch "${ODOO_BRANCH}" --depth 1 "${ODOO_REPO}" "${ODOO_DIR}"
fi

sed -i 's/^\(gevent\b\)/#\1/' "${ODOO_DIR}/requirements.txt"
sed -i 's/^\(lxml\b\)/#\1/' "${ODOO_DIR}/requirements.txt"
sed -i 's/^\(pillow\b\)/#\1/' "${ODOO_DIR}/requirements.txt"
sed -i 's/^\(psycopg2\b\)/#\1/' "${ODOO_DIR}/requirements.txt"
sed -i 's/^\(python-ldap\b\)/#\1/' "${ODOO_DIR}/requirements.txt"
sed -i 's/^\(greenlet\b\)/#\1/' "${ODOO_DIR}/requirements.txt"

#
echo "=== 2. Création du virtualenv Python et installation des dépendances ==="
# Odoo 16.0 requires Python <= 3.12 (cgi module removed in 3.13)
if command -v python3.12 &>/dev/null; then
    PYTHON_BIN="python3.12"
elif command -v python3.11 &>/dev/null; then
    PYTHON_BIN="python3.11"
elif command -v python3.10 &>/dev/null; then
    PYTHON_BIN="python3.10"
else
    PYTHON_BIN="python3"
    echo "WARNING: Python 3.10-3.12 not found, falling back to $(${PYTHON_BIN} --version). May need legacy-cgi shim."
fi
echo "Utilisation de : $PYTHON_BIN ($(${PYTHON_BIN} --version))"
"${PYTHON_BIN}" -m venv "${ODOO_DIR}/.venv"
"${ODOO_DIR}/.venv/bin/pip" install --upgrade pip "setuptools<80" wheel
"${ODOO_DIR}/.venv/bin/pip" install -r "${ODOO_DIR}/requirements.txt" --ignore-requires-python || true

echo "=== 3. Installation des dépendances Python additionnelles ==="
PY_VERSION=$("${ODOO_DIR}/.venv/bin/python3" -c "import sys; print(sys.version_info >= (3,13))")
if [ "$PY_VERSION" = "True" ]; then
    echo "Python >= 3.13 détecté : installation du shim legacy-cgi"
    "${ODOO_DIR}/.venv/bin/pip" install legacy-cgi
fi
"${ODOO_DIR}/.venv/bin/pip" install openpyxl translate nltk pillow
"${ODOO_DIR}/.venv/bin/pip" install gevent greenlet "werkzeug>=2.1,<3" lxml lxml_html_clean pillow psycopg2-binary pypdf2

echo "=== Téléchargement des données NLTK ==="
"${ODOO_DIR}/.venv/bin/python3" -c "import nltk; nltk.download('punkt')"

echo "=== 4. Création du binaire /usr/local/bin/odoo ==="
sudo tee "${ODOO_BIN}" > /dev/null <<'EOF'
#!/bin/bash
cd /var/www/html/odoo/
/var/www/html/odoo/.venv/bin/python3 /var/www/html/odoo/odoo-bin --config=/var/www/html/odoo/odoo.conf
EOF
sudo chmod +x "${ODOO_BIN}"

echo "=== 5. Création du service systemd ==="
sudo tee "${SERVICE_FILE}" > /dev/null <<EOF
[Unit]
Description=Odoo
#Requires=postgresql.service
#After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo
PermissionsStartOnly=true
User=${ODOO_USER}
Group=${ODOO_GROUP}
ExecStart=/usr/local/bin/odoo

[Install]
WantedBy=multi-user.target
EOF

echo "=== 6. Création de odoo.conf ==="
sudo mkdir -p "${ODOO_DIR}/log"
sudo chown "${ODOO_OWNER}" "${ODOO_DIR}/log"

sudo tee "${ODOO_DIR}/odoo.conf" > /dev/null <<'EOF'
[options]
admin_passwd = $pbkdf2-sha512$25000$nfNeKyVkTKnVWitlTEnpnQ$69yRkdQZeNmjBNZ4vtmIrc5ShapHR8/.qYElQlAX1bQaQZboI79rJpw21VyDFLfOVDAB3JsIRhZIJgHF.6GCig
db_host = localhost
db_port = False
db_user = odoo
db_password = __DB_PASSWORD__
db_filter = .*
addons_path = /var/www/html/odoo/odoo-oaas-addons,/var/www/html/odoo/addons
limit_memory_hard = 1677721600
limit_memory_soft = 629145600
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200
max_cron_threads = 1
workers = 8
proxy_mode = True
logfile = /var/www/html/odoo/log/odoo-server.log
pidfile = /var/www/html/odoo/odoo.pid
EOF
sudo sed -i "s/__DB_PASSWORD__/${ODOO_DB_PASSWORD}/" "${ODOO_DIR}/odoo.conf"
sudo chown "${ODOO_OWNER}" "${ODOO_DIR}/odoo.conf"
sudo chmod 640 "${ODOO_DIR}/odoo.conf"

if [ -n "${PROD_BACKUP_ZIP}" ]; then
    echo "=== 7. Installation de la base ${ODOO_DB_NAME} depuis ${PROD_BACKUP_ZIP} ==="
    RESTORE_TMP="$(mktemp -d)"
    trap 'rm -rf "${RESTORE_TMP}"' EXIT

    echo "-> Extraction du zip"
    unzip -q "${PROD_BACKUP_ZIP}" -d "${RESTORE_TMP}"

    DUMP_FILE="${RESTORE_TMP}/dump.sql"
    FILESTORE_SRC="${RESTORE_TMP}/filestore"
    [ -f "${DUMP_FILE}" ] || {
        echo "dump.sql introuvable dans le zip — format inattendu (attendu : export" >&2
        echo "standard Odoo, zip contenant dump.sql + filestore/)" >&2
        exit 1
    }

    echo "-> (Re)création de la base ${ODOO_DB_NAME}"
    PGPASSWORD="${ODOO_DB_PASSWORD}" dropdb -h localhost -U odoo --if-exists "${ODOO_DB_NAME}"
    PGPASSWORD="${ODOO_DB_PASSWORD}" createdb -h localhost -U odoo -O odoo "${ODOO_DB_NAME}"

    echo "-> Import du dump SQL (peut prendre plusieurs minutes selon la taille de la base)"
    PGPASSWORD="${ODOO_DB_PASSWORD}" psql -h localhost -U odoo -d "${ODOO_DB_NAME}" \
        -q -v ON_ERROR_STOP=1 -f "${DUMP_FILE}"

    if [ -d "${FILESTORE_SRC}" ]; then
        FILESTORE_DST="/home/${ODOO_USER}/.local/share/Odoo/filestore/${ODOO_DB_NAME}"
        echo "-> Restauration du filestore vers ${FILESTORE_DST}"
        echo "   (chemin par défaut Odoo, data_dir non fixé dans odoo.conf — à vérifier"
        echo "   si ce comportement change un jour)"
        sudo mkdir -p "$(dirname "${FILESTORE_DST}")"
        sudo rm -rf "${FILESTORE_DST}"
        sudo cp -r "${FILESTORE_SRC}" "${FILESTORE_DST}"
        sudo chown -R "${ODOO_OWNER}" "${FILESTORE_DST}"
    else
        echo "-> Pas de filestore/ dans le zip, ignoré."
    fi

    rm -rf "${RESTORE_TMP}"
    trap - EXIT

    echo "!! Base restaurée telle quelle depuis un export production : tokens/clés API"
    echo "   (LinkedIn, IA...) et données réelles présents tel quel sur cet environnement."
    echo "   Neutraliser manuellement avant de considérer les intégrations sortantes sûres"
    echo "   à tester (voir migration-odoo19/03-risques-infra.md)."
else
    echo "=== 7. Installation de la base : sautée (aucun zip fourni) ==="
fi

echo "=== 8. Déploiement des addons OAAS ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADDONS_DIR="${ODOO_DIR}/odoo-oaas-addons"

sudo mkdir -p "${ADDONS_DIR}"
sudo cp -r "${SCRIPT_DIR}"/. "${ADDONS_DIR}/"
sudo chown -R "${ODOO_OWNER}" "${ADDONS_DIR}"

echo "=== 9. Patches compatibilité Python 3.14 ==="
"${ODOO_DIR}/.venv/bin/python3" - <<'PYEOF'
import sys

patches = [
    # safe_eval.py : LOAD_SMALL_INT dans _CONST_OPCODES (remplace LOAD_CONST pour petits entiers)
    {
        "file": "/var/www/html/odoo/odoo/tools/safe_eval.py",
        "marker": "    'LOAD_SMALL_INT',",
        "search": "    # 3.13\n    'TO_BOOL',\n])) - _BLACKLIST",
        "replace": "    # 3.13\n    'TO_BOOL',\n    # 3.14 https://docs.python.org/3/whatsnew/3.14.html\n    'LOAD_SMALL_INT',\n])) - _BLACKLIST",
    },
    # safe_eval.py : NOT_TAKEN + POP_ITER + nouveaux opcodes 3.14 dans _SAFE_OPCODES
    {
        "file": "/var/www/html/odoo/odoo/tools/safe_eval.py",
        "marker": "    'NOT_TAKEN',\n    'POP_ITER',",
        "search": "    # 3.13\n    'CALL_KW', 'LOAD_FAST_LOAD_FAST',\n    'STORE_FAST_STORE_FAST', 'STORE_FAST_LOAD_FAST',\n    'CONVERT_VALUE', 'FORMAT_SIMPLE', 'FORMAT_WITH_SPEC',\n    'SET_FUNCTION_ATTRIBUTE',\n])) - _BLACKLIST",
        "replace": "    # 3.13\n    'CALL_KW', 'LOAD_FAST_LOAD_FAST',\n    'STORE_FAST_STORE_FAST', 'STORE_FAST_LOAD_FAST',\n    'CONVERT_VALUE', 'FORMAT_SIMPLE', 'FORMAT_WITH_SPEC',\n    'SET_FUNCTION_ATTRIBUTE',\n    # 3.14 https://docs.python.org/3/whatsnew/3.14.html\n    'NOT_TAKEN',\n    'POP_ITER',\n    'LOAD_FAST_BORROW', 'LOAD_FAST_BORROW_LOAD_FAST_BORROW',\n    'JUMP_IF_FALSE', 'JUMP_IF_TRUE',\n])) - _BLACKLIST",
    },
    # ir_qweb.py : NOT_TAKEN + POP_ITER dans _SAFE_QWEB_OPCODES
    {
        "file": "/var/www/html/odoo/odoo/addons/base/models/ir_qweb.py",
        "marker": "    'NOT_TAKEN',",
        "search": "    'SET_FUNCTION_ATTRIBUTE',\n])) - _BLACKLIST",
        "replace": "    'SET_FUNCTION_ATTRIBUTE',\n    # 3.14 https://docs.python.org/3/whatsnew/3.14.html\n    'NOT_TAKEN',\n    'POP_ITER',\n])) - _BLACKLIST",
    },
    # view_validation.py : ast.Str → ast.Constant (supprimé en Python 3.12+)
    {
        "file": "/var/www/html/odoo/odoo/tools/view_validation.py",
        "marker": "isinstance(key, ast.Constant) and isinstance(key.value, str)",
        "search": "    if not all(isinstance(key, ast.Str) for key in expr.keys):\n        raise ValueError(\"Non-string literal dict key\")\n    return {key.s: val for key, val in zip(expr.keys, expr.values)}",
        "replace": "    if not all(isinstance(key, ast.Constant) and isinstance(key.value, str) for key in expr.keys):\n        raise ValueError(\"Non-string literal dict key\")\n    return {key.value: val for key, val in zip(expr.keys, expr.values)}",
    },
    {
        "file": "/var/www/html/odoo/odoo/tools/view_validation.py",
        "marker": "isinstance(elem, ast.Constant) and isinstance(elem.value, str)",
        "search": "            if isinstance(elem, ast.Str):\n                # note: this doesn't check the and/or structure\n                _check(elem.s in ('&', '|', '!'),\n                       f\"logical operators should be '&', '|', or '!', found {elem.s!r}\")\n                continue",
        "replace": "            if isinstance(elem, ast.Constant) and isinstance(elem.value, str):\n                # note: this doesn't check the and/or structure\n                _check(elem.value in ('&', '|', '!'),\n                       f\"logical operators should be '&', '|', or '!', found {elem.value!r}\")\n                continue",
    },
    {
        "file": "/var/www/html/odoo/odoo/tools/view_validation.py",
        "marker": "isinstance(operator, ast.Constant) and isinstance(operator.value, str)",
        "search": "            _check(isinstance(operator, ast.Str),\n                   f\"operator should be a string, found {type(operator).__name__}\")\n            if isinstance(lhs, ast.Str):\n                fnames.add(lhs.s)",
        "replace": "            _check(isinstance(operator, ast.Constant) and isinstance(operator.value, str),\n                   f\"operator should be a string, found {type(operator).__name__}\")\n            if isinstance(lhs, ast.Constant) and isinstance(lhs.value, str):\n                fnames.add(lhs.value)",
    },
    # ir_ui_view.py : ast.Str → ast.Constant
    {
        "file": "/var/www/html/odoo/odoo/addons/base/models/ir_ui_view.py",
        "marker": "isinstance(val_ast, ast.Constant) and isinstance(val_ast.value, str)",
        "search": "                        if not isinstance(val_ast, ast.Str):\n                            msg = _(\n                                '\"group_by\" value must be a string %(attribute)s=%(value)r',\n                                attribute=attr, value=expr,\n                            )\n                            self._raise_view_error(msg, node)\n                        group_by = val_ast.s",
        "replace": "                        if not (isinstance(val_ast, ast.Constant) and isinstance(val_ast.value, str)):\n                            msg = _(\n                                '\"group_by\" value must be a string %(attribute)s=%(value)r',\n                                attribute=attr, value=expr,\n                            )\n                            self._raise_view_error(msg, node)\n                        group_by = val_ast.value",
    },
]

for p in patches:
    with open(p["file"]) as f:
        content = f.read()
    if p["marker"] in content:
        print(f"  [ok] {p['file']} déjà patché")
        continue
    if p["search"] not in content:
        print(f"  [warn] {p['file']} : ancre introuvable, patch ignoré", file=sys.stderr)
        continue
    with open(p["file"], "w") as f:
        f.write(content.replace(p["search"], p["replace"]))
    print(f"  [patché] {p['file']}")
PYEOF

echo "=== 10. Activation et démarrage du service Odoo ==="
sudo systemctl daemon-reload
sudo systemctl enable odoo
sudo systemctl restart odoo

echo "=== 11. Configuration Apache (Ubuntu / apache2, vhost dédié ${APACHE_DOMAIN}) ==="
APACHE_SITE_FILE="/etc/apache2/sites-available/${APACHE_DOMAIN}.conf"

sudo a2enmod proxy proxy_http proxy_wstunnel rewrite headers expires > /dev/null

# Heredoc entièrement quoté : les placeholders Apache (%{...}, ${APACHE_LOG_DIR})
# doivent rester littéraux, seul __DOMAIN__ est substitué ensuite via sed.
sudo tee "${APACHE_SITE_FILE}" > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerName __DOMAIN__

    ProxyPassMatch /hooks !
    ProxyPassMatch /mail !
    ProxyPass / http://127.0.0.1:8069/
    ProxyPassReverse / http://127.0.0.1:8069/

    <Location /websocket>
      ProxyPass http://odoochat
      ProxyPassReverse http://odoochat

      RewriteEngine On
      RewriteCond %{HTTP:Upgrade} =websocket [NC]
      RewriteRule /(.*) ws://odoochat/$1 [P,L]

      RequestHeader set Upgrade "websocket"
      RequestHeader set Connection "Upgrade"
      RequestHeader set X-Forwarded-Host "%{Host}i"
      RequestHeader set X-Forwarded-For "%{proxy:clientip}i"
      RequestHeader set X-Forwarded-Proto "%{scheme}e"
      RequestHeader set X-Real-IP "%{REMOTE_ADDR}e"
    </Location>

    Alias /static/ /var/www/html/odoo/addons/static/
    Alias /web/ /var/www/html/odoo/web/

    <Directory /var/www/html/odoo/addons/static/>
       Options FollowSymLinks
       ExpiresActive On
       ExpiresDefault "access plus 1 day"
    </Directory>

    <Location /web/database>
       Require all granted
    </Location>

    ErrorLog ${APACHE_LOG_DIR}/__DOMAIN__-error.log
    CustomLog ${APACHE_LOG_DIR}/__DOMAIN__-access.log combined
</VirtualHost>
EOF
sudo sed -i "s/__DOMAIN__/${APACHE_DOMAIN}/g" "${APACHE_SITE_FILE}"

sudo a2ensite "${APACHE_DOMAIN}" > /dev/null
echo "Vhost créé et activé : ${APACHE_SITE_FILE}"

if systemctl is-active --quiet apache2 2>/dev/null; then
    sudo apache2ctl configtest
    sudo systemctl reload apache2
    echo "Apache rechargé (${APACHE_DOMAIN})."
else
    echo "apache2 non actif — à démarrer manuellement (sudo systemctl start apache2)."
fi

echo "=== 12. Certificat SSL (Let's Encrypt) pour ${APACHE_DOMAIN} ==="
if [ -n "${LETSENCRYPT_EMAIL}" ]; then
    if ! command -v certbot &>/dev/null; then
        echo "-> certbot absent, installation"
        sudo apt-get install -y certbot python3-certbot-apache
    fi
    echo "-> Demande du certificat via le plugin Apache de certbot"
    sudo certbot --apache -d "${APACHE_DOMAIN}" --non-interactive --agree-tos \
        -m "${LETSENCRYPT_EMAIL}" --redirect
    echo "Certificat SSL obtenu, vhost basculé en HTTPS avec redirection depuis le HTTP."
    echo "Renouvellement automatique via le timer systemd certbot.timer (standard Ubuntu)."
else
    echo "Aucun email fourni à l'étape de config — certificat SSL sauté (vhost HTTP uniquement)."
fi

echo ""
echo "=== Déploiement terminé ==="
echo "Statut du service :"
sudo systemctl status odoo --no-pager

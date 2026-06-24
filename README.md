# odoo-oaas-addons



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/bprunier/odoo-oaas-addons.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/bprunier/odoo-oaas-addons/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.


##Deploy
A FAIRE LE DEPLOY!!!!
git clone https://github.com/odoo/odoo.git version 16 Odoo Server 16.0


  GNU nano 5.6.1                                                  /etc/systemd/system/odoo.service                                                            
[Unit]
Description=Odoo
#Requires=postgresql.service
#After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo
PermissionsStartOnly=true
User=ben
Group=apache
ExecStart=/usr/local/bin/odoo

[Install]
WantedBy=multi-user.target


  GNU nano 5.6.1                                                         /usr/local/bin/odoo                                                                  
#! /bin/bash
cd /var/www/html/odoo/
/var/www/html/odoo/.venv/bin/python3 /var/www/html/odoo/odoo-bin --config=/var/www/html/odoo/odoo.conf

#python3 odoo-bin -c odoo.conf 
#python3 odoo-bin -c odoo.conf  > /dev/null &
#source /var/www/html/odoo/.venv/bin/activate && python3 /var/www/html/odoo/odoo-bin -c /var/www/html/odoo/odoo.conf &
#cd /var/www/html/odoo-3D/release/server/lw-web-server/
#yarn run start > /dev/null &


  GNU nano 5.6.1                                                    /var/www/html/odoo/odoo.conf                                                              
[options]
admin_passwd = $pbkdf2-sha512$25000$nfNeKyVkTKnVWitlTEnpnQ$69yRkdQZeNmjBNZ4vtmIrc5ShapHR8/.qYElQlAX1bQaQZboI79rJpw21VyDFLfOVDAB3JsIRhZIJgHF.6GCig
db_host = localhost
db_port = False
db_user = odoo
db_password = Maison63#123
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


ATTENTION 


ProxyPassMatch /hooks !
  ProxyPassMatch /mail !
  ProxyPass / http://127.0.0.1:{{ host.data.get('odoo_port') }}/
  ProxyPassReverse / http://127.0.0.1:{{ host.data.get('odoo_port') }}/
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
     Require ip {{ host.data.get('admin_allowed_ip', '127.0.0.1') }}
  </Location>



### A FAIRE MANUELLEMENT DANS LE FICHIER ODOO.CONF et .venv
1
sudo su odoo
Ensuite, entrer dans le shell Python avec la commande :

1
python3
Quand vous avez le signe supérieur 3 fois >>>, vous êtes dans le shell python. Vous pouvez ensuite importer les modules de hachage comme suit :

1
>>> from passlib.context import CryptContext
Puis vous pouvez crypter le nouveau mot de passe en utilisant le PBKDF2 SHA512 par exemple et afficher le résultat comme indiqué ci-dessous :

1
>>> print(CryptContext(schemes=['pbkdf2_sha512']).encrypt('Votre_nouveau_mot_de_passe'))
Il est à noter que Votre_nouveau_mot_de_passe est le nouveau mot de passe que vous voulez avoir, donc n’oubliez pas de le changer.

Une fois que vous avez tapé sur la touche Entrée, vous allez avoir une longue chaîne de caractère qui va s’afficher, c’est votre mot de passe qui est haché et qui va être par la suite enregistré dans votre base de données. Cette longue chaîne de caractère est de la forme :

1
$pbkdf2-sha512$25000$IgQgZEzpHeP8nxMiJOT8nw$7Bo.o9RI5FlMgZndgEN0ZS60mqlF7xLZ0zVgeILPscDO7U8somJO4ZQPDXmIeAbSmhxKcmW4Z3MCqojelpsBww
Copiez cette longue chaîne de caractère. Nous allons l’utiliser un peu plus tard.

Quittez ensuite le shell python avec la commande :

1
>>> exit()
Et quittez ensuite l’utilisateur odoo avec la commande :

1
$ exit

ensuite accéder à : http://localhost:8069/web/database/selector

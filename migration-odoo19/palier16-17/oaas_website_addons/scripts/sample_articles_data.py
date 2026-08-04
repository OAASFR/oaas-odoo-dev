# -*- coding: utf-8 -*-
"""
Donnees des articles de blog d'exemple (OAAS), utilisees par
make_sample_xlsx.py pour generer OAAS_BLOG_POST_IOTPlatform.xlsx au format
d'import courant (feuille "Blog import", 31 colonnes 0-indexees).

Chaque article est un dict avec, pour chaque champ traduisible, une cle EN et
une cle FR (suffixe _fr). Les contenus Why/How/What/Conclusion/Summary sont du
HTML builder Odoo insere tel quel. Les colonnes image (cover/why/how/what/
conclusion) sont laissees vides : les images embarquees sont recollees dans le
xlsx ensuite.

L'accordeon "Your benefits" / "Vos benefices" partage une structure commune :
seul le LIBELLE du premier item change d'un article a l'autre (cf. PDF source).
On factorise donc la generation de l'accordeon via _advantages()/_advantages_fr().
"""


def _advantages(first_label):
    # Accordeon EN. Le premier item porte le libelle propre a l'article ;
    # les items suivants sont les benefices generiques de la plateforme.
    return (
        '<h3>Your benefits</h3>'
        '<div id="myCollapse" class="accordion" role="tablist">'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="true" class="card-header s_faq_collapse_right_icon" data-bs-target="#myCollapseTab1">' + first_label + '</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab1" class="collapse show">'
        '<div class="card-body"><p class="card-text">OAAS relies on a proven technical foundation: device or data management, collection, dashboards, alerts, security and automation. You save development time and focus your effort on business needs.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab2">Reusable foundation</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab2" class="collapse">'
        '<div class="card-body"><p class="card-text">Instead of rebuilding a complete solution for every project, OAAS relies on a scalable technical foundation that can adapt to different uses, industries and field constraints.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab3">Centralized management</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab3" class="collapse">'
        '<div class="card-body"><p class="card-text">All elements are monitored from a single interface. Teams can review status, latest data and configuration without multiplying tools.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab4">Actionable data</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab4" class="collapse">'
        '<div class="card-body"><p class="card-text">Field data is collected, historized and transformed into understandable indicators. The goal is not only to store measurements, but to make them useful for decisions and actions.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab5">Reliable delivery</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab5" class="collapse">'
        '<div class="card-body"><p class="card-text">Clear specifications, controlled testing and close collaboration keep delivery focused, testable and aligned with the real needs of the field.</p></div>'
        '</div></div>'
        '</div>'
    )


def _advantages_fr(first_label):
    # Accordeon FR : meme structure, libelles traduits.
    return (
        '<h3>Vos bénéfices</h3>'
        '<div id="myCollapse" class="accordion" role="tablist">'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="true" class="card-header s_faq_collapse_right_icon" data-bs-target="#myCollapseTab1">' + first_label + '</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab1" class="collapse show">'
        '<div class="card-body"><p class="card-text">OAAS s’appuie sur une base technique éprouvée : gestion des appareils ou des données, collecte, tableaux de bord, alertes, sécurité et automatisation. Vous gagnez du temps de développement et concentrez vos efforts sur les besoins métier.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab2">Base réutilisable</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab2" class="collapse">'
        '<div class="card-body"><p class="card-text">Plutôt que de reconstruire une solution complète pour chaque projet, OAAS s’appuie sur une base technique évolutive qui s’adapte à différents usages, secteurs et contraintes de terrain.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab3">Gestion centralisée</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab3" class="collapse">'
        '<div class="card-body"><p class="card-text">Tous les éléments sont supervisés depuis une seule interface. Les équipes consultent l’état, les dernières données et la configuration sans multiplier les outils.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab4">Données exploitables</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab4" class="collapse">'
        '<div class="card-body"><p class="card-text">Les données du terrain sont collectées, historisées et transformées en indicateurs compréhensibles. L’objectif n’est pas seulement de stocker des mesures, mais de les rendre utiles pour les décisions et les actions.</p></div>'
        '</div></div>'
        '<div class="card bg-white" data-name="Item">'
        '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab5">Livraison fiable</a>'
        '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab5" class="collapse">'
        '<div class="card-body"><p class="card-text">Des spécifications claires, des tests maîtrisés et une collaboration étroite gardent la livraison ciblée, testable et alignée sur les besoins réels du terrain.</p></div>'
        '</div></div>'
        '</div>'
    )


# Auteur et website communs a tous les articles (cf. PDF).
AUTHOR_EMAIL = "bprunier@oaas.fr"
WEBSITE = "OAAS"

# Les 13 articles, dans l'ordre du PDF. Champs traduits : *_fr.
# Les images sont laissees vides (recollees dans le xlsx ensuite).
ARTICLES = [
    # 1 ----------------------------------------------------------------------
    {
        "blog": "Platforms",
        "title": "IOTPlatform: a programmable IoT platform for connected devices",
        "title_fr": "IOTPlatform : une plateforme IoT programmable pour appareils connectés",
        "subtitle": "The first programmable IoT platform for managing, monitoring and remotely controlling your connected devices",
        "subtitle_fr": "La première plateforme IoT programmable pour gérer, superviser et piloter à distance vos appareils connectés",
        "post_date": "17/09/2024 00:00:08",
        "meta_title": "Programmable IoT Platform | Manage & Monitor Devices | OAAS",
        "meta_description": "IOTPlatform by OAAS centralizes management, monitoring and remote control of your connected devices. Collect data, automate actions and scale IoT projects faster.",
        "meta_keywords": "IoT platform, programmable IoT, device management, remote monitoring, IoT automation, connected devices, LoRa, Sigfox, OAAS",
        "meta_title_fr": "Plateforme IoT programmable | Gérer et superviser vos appareils | OAAS",
        "meta_description_fr": "IOTPlatform d’OAAS centralise la gestion, la supervision et le pilotage à distance de vos appareils connectés. Collectez vos données, automatisez vos actions et déployez vos projets IoT plus vite.",
        "meta_keywords_fr": "plateforme IoT, IoT programmable, gestion d’appareils, supervision à distance, automatisation IoT, appareils connectés, LoRa, Sigfox, OAAS",
        "why": (
            "<h3>Why build a programmable IoT platform?</h3>"
            "<p>An <strong>IoT project</strong> often starts simply: read a temperature, track "
            "a level, measure a consumption or trigger a device remotely. At this stage, a "
            "script or a simple dashboard is often enough.</p>"
            "<p>But as soon as the project grows, the needs become more complex: several "
            "devices, several users, several sites, access rights, history, alerts and business "
            "rules. Maintaining a custom-built tool quickly becomes costly and fragile.</p>"
            "<p><strong>IOTPlatform</strong> answers this need by centralizing the management "
            "of connected equipment in a single, adaptable and scalable solution.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi construire une plateforme IoT programmable ?</h3>"
            "<p>Un <strong>projet IoT</strong> commence souvent simplement : relever une "
            "température, suivre un niveau, mesurer une consommation ou déclencher un "
            "équipement à distance. À ce stade, un script ou un simple tableau de bord suffit "
            "souvent.</p>"
            "<p>Mais dès que le projet grandit, les besoins se complexifient : plusieurs "
            "appareils, plusieurs utilisateurs, plusieurs sites, droits d’accès, historique, "
            "alertes et règles métier. Maintenir un outil sur-mesure devient vite coûteux et "
            "fragile.</p>"
            "<p><strong>IOTPlatform</strong> répond à ce besoin en centralisant la gestion des "
            "équipements connectés dans une seule solution adaptable et évolutive.</p>"
        ),
        "how": (
            "<h3>How does the platform work?</h3>"
            "<p>The platform relies on a simple logic: <strong>connect, collect, visualize and "
            "automate</strong>. Each step builds on the previous one to turn raw signals into "
            "decisions.</p>"
            "<p>First, devices are added in the interface. Then they send their data, which is "
            "stored, historized and displayed in readable dashboards. Finally, the user can "
            "create scenarios: send an alert, trigger an action or connect another tool via the "
            "API.</p>"
        ),
        "how_fr": (
            "<h3>Comment fonctionne la plateforme ?</h3>"
            "<p>La plateforme repose sur une logique simple : <strong>connecter, collecter, "
            "visualiser et automatiser</strong>. Chaque étape s’appuie sur la précédente pour "
            "transformer des signaux bruts en décisions.</p>"
            "<p>D’abord, les appareils sont ajoutés dans l’interface. Ensuite, ils envoient "
            "leurs données, qui sont stockées, historisées et affichées dans des tableaux de "
            "bord lisibles. Enfin, l’utilisateur peut créer des scénarios : envoyer une alerte, "
            "déclencher une action ou connecter un autre outil via l’API.</p>"
        ),
        "what": (
            "<h3>What can you build with this platform?</h3>"
            "<p>The platform can be used for many IoT use cases: building supervision, energy "
            "monitoring, connected maintenance, actuator control, alert management, multi-site "
            "monitoring or environmental surveillance.</p>"
        ),
        "what_fr": (
            "<h3>Que pouvez-vous construire avec cette plateforme ?</h3>"
            "<p>La plateforme peut servir à de nombreux cas d’usage IoT : supervision de "
            "bâtiment, suivi énergétique, maintenance connectée, pilotage d’actionneurs, "
            "gestion d’alertes, suivi multi-sites ou surveillance environnementale.</p>"
        ),
        "conclusion": (
            "<p>With its programmable IoT platform, OAAS offers a foundation able to connect "
            "devices, collect data, automate actions and build interfaces tailored to business "
            "needs.</p>"
            "<p>Whether you are starting your first connected project or industrializing an "
            "existing fleet, IOTPlatform gives you a reliable base to grow on.</p>"
        ),
        "conclusion_fr": (
            "<p>Avec sa plateforme IoT programmable, OAAS offre une base capable de connecter "
            "les appareils, collecter les données, automatiser les actions et construire des "
            "interfaces adaptées aux besoins métier.</p>"
            "<p>Que vous démarriez votre premier projet connecté ou que vous industrialisiez un "
            "parc existant, IOTPlatform vous donne une base fiable pour grandir.</p>"
        ),
        "summary": (
            "<p><strong>IOTPlatform</strong> is a programmable IoT platform that centralizes the "
            "management, monitoring and remote control of your connected devices. This article "
            "explains why such a platform matters, how it works, what you can build with it, and "
            "how to start your first use case in minutes rather than months.</p>"
        ),
        "summary_fr": (
            "<p><strong>IOTPlatform</strong> est une plateforme IoT programmable qui centralise "
            "la gestion, la supervision et le pilotage à distance de vos appareils connectés. "
            "Cet article explique pourquoi une telle plateforme compte, comment elle fonctionne, "
            "ce que vous pouvez construire avec, et comment lancer votre premier cas d’usage en "
            "quelques minutes plutôt qu’en quelques mois.</p>"
        ),
        "adv_label": "Lower development costs",
        "adv_label_fr": "Réduction des coûts de développement",
    },
    # 2 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Fleet: real-time tire wear monitoring for vehicle fleets",
        "title_fr": "Fleet : suivi de l’usure des pneus en temps réel pour flottes de véhicules",
        "subtitle": "An IoT data platform that turns tire measurements into actionable maintenance insights",
        "subtitle_fr": "Une plateforme de données IoT qui transforme les mesures de pneus en informations de maintenance exploitables",
        "post_date": "12/02/2024 00:00:00",
        "meta_title": "Real-Time Tire Wear Monitoring Platform | OAAS",
        "meta_description": "OAAS built an IoT platform that collects tire measurements, estimates wear in real time and helps customers manage vehicle fleets from one secure interface.",
        "meta_keywords": "tire wear monitoring, fleet management, IoT platform, real-time data, predictive maintenance, Django, OAAS",
        "meta_title_fr": "Plateforme de suivi de l’usure des pneus en temps réel | OAAS",
        "meta_description_fr": "OAAS a construit une plateforme IoT qui collecte les mesures de pneus, estime l’usure en temps réel et aide les clients à gérer leurs flottes de véhicules depuis une seule interface sécurisée.",
        "meta_keywords_fr": "suivi de l’usure des pneus, gestion de flotte, plateforme IoT, données temps réel, maintenance prédictive, Django, OAAS",
        "why": (
            "<h3>Why digitize tire wear monitoring?</h3>"
            "<p>Tire wear has a direct impact on safety, maintenance costs and fleet "
            "availability. The client had developed a dedicated measurement device and an "
            "algorithm, but needed a reliable platform to turn those measurements into "
            "operational information.</p>"
            "<p>The project therefore had to connect field equipment, store measurements and "
            "make wear estimates usable by fleet managers.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi digitaliser le suivi de l’usure des pneus ?</h3>"
            "<p>L’usure des pneus a un impact direct sur la sécurité, les coûts de maintenance "
            "et la disponibilité des flottes. Le client avait développé un appareil de mesure "
            "dédié et un algorithme, mais avait besoin d’une plateforme fiable pour transformer "
            "ces mesures en informations opérationnelles.</p>"
            "<p>Le projet devait donc connecter les équipements de terrain, stocker les mesures "
            "et rendre les estimations d’usure exploitables par les gestionnaires de flotte.</p>"
        ),
        "how": (
            "<h3>How was the platform built?</h3>"
            "<p>OAAS first created the data acquisition layer used to retrieve measurements "
            "from the specialized tire-wear tool. Incoming records were timestamped and "
            "processed as soon as they reached the platform.</p>"
            "<p>A tire-reference database was then introduced to manage the diversity of models "
            "and characteristics, and the wear-estimation algorithm was integrated to produce "
            "real-time results.</p>"
        ),
        "how_fr": (
            "<h3>Comment la plateforme a-t-elle été construite ?</h3>"
            "<p>OAAS a d’abord créé la couche d’acquisition de données servant à récupérer les "
            "mesures de l’outil spécialisé d’usure des pneus. Les enregistrements entrants "
            "étaient horodatés et traités dès leur arrivée sur la plateforme.</p>"
            "<p>Une base de référence des pneus a ensuite été introduite pour gérer la "
            "diversité des modèles et caractéristiques, et l’algorithme d’estimation de l’usure "
            "a été intégré pour produire des résultats en temps réel.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>The application was developed with Django and web technologies, then hosted and "
            "operated by OAAS between 2019 and 2022.</p>"
            "<p>Its architecture was designed to support high volumes of measurements while "
            "keeping acquisition, processing and customer consultation responsive.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>L’application a été développée avec Django et des technologies web, puis "
            "hébergée et exploitée par OAAS entre 2019 et 2022.</p>"
            "<p>Son architecture a été conçue pour supporter de gros volumes de mesures tout en "
            "gardant l’acquisition, le traitement et la consultation client réactifs.</p>"
        ),
        "conclusion": (
            "<p>The project gave customers a safer and more consistent way to monitor tire "
            "condition across their fleets.</p>"
            "<p>By combining connected measurements, reference data and real-time processing, "
            "the platform transformed a specialized device into a complete fleet-maintenance "
            "service.</p>"
        ),
        "conclusion_fr": (
            "<p>Le projet a offert aux clients un moyen plus sûr et plus cohérent de surveiller "
            "l’état des pneus sur l’ensemble de leurs flottes.</p>"
            "<p>En combinant mesures connectées, données de référence et traitement en temps "
            "réel, la plateforme a transformé un appareil spécialisé en un service complet de "
            "maintenance de flotte.</p>"
        ),
        "summary": (
            "<p>OAAS designed a real-time IoT platform for monitoring tire wear across vehicle "
            "fleets. The solution combines specialized measurement equipment, a structured tire "
            "database and an estimation algorithm in a secure customer portal.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a conçu une plateforme IoT temps réel pour surveiller l’usure des pneus sur "
            "des flottes de véhicules. La solution combine un équipement de mesure spécialisé, "
            "une base de données de pneus structurée et un algorithme d’estimation dans un "
            "portail client sécurisé.</p>"
        ),
        "adv_label": "Faster maintenance decisions",
        "adv_label_fr": "Décisions de maintenance plus rapides",
    },
    # 3 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Innovapeek: RFID traceability for orthodontic instruments",
        "title_fr": "Innovapeek : traçabilité RFID des instruments orthodontiques",
        "subtitle": "A mobile RFID platform for tracking sterilization workflows",
        "subtitle_fr": "Une plateforme RFID mobile pour suivre les flux de stérilisation",
        "post_date": "12/02/2024 00:00:01",
        "meta_title": "RFID Sterilization Traceability Platform | OAAS",
        "meta_description": "OAAS created a mobile RFID proof of concept to trace orthodontic instruments through cleaning, sterilization and packaging workflows.",
        "meta_keywords": "RFID traceability, sterilization tracking, orthodontic instruments, CAEN RFID, Raspberry Pi, 4G, OAAS",
        "meta_title_fr": "Plateforme de traçabilité RFID de stérilisation | OAAS",
        "meta_description_fr": "OAAS a créé une preuve de concept RFID mobile pour tracer les instruments orthodontiques tout au long des flux de nettoyage, de stérilisation et de conditionnement.",
        "meta_keywords_fr": "traçabilité RFID, suivi de stérilisation, instruments orthodontiques, RFID CAEN, Raspberry Pi, 4G, OAAS",
        "why": (
            "<h3>Why trace each sterilization step?</h3>"
            "<p>Sterilization quality depends on knowing where each instrument is, which "
            "operations it has completed and whether the complete process can be "
            "demonstrated.</p>"
            "<p>The objective was to identify orthodontic instruments automatically and create "
            "a reliable digital history without slowing down cabinet operations.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi tracer chaque étape de stérilisation ?</h3>"
            "<p>La qualité de la stérilisation dépend de savoir où se trouve chaque instrument, "
            "quelles opérations il a subies et si l’on peut démontrer le processus complet.</p>"
            "<p>L’objectif était d’identifier automatiquement les instruments orthodontiques et "
            "de créer un historique numérique fiable sans ralentir le travail du cabinet.</p>"
        ),
        "how": (
            "<h3>How did the RFID solution work?</h3>"
            "<p>The client first validated the integration of two RFID tags in each instrument "
            "so that at least one tag could be read accurately in normal operating "
            "conditions.</p>"
            "<p>OAAS then integrated CAEN RFID readers with the platform and modeled the "
            "successive workflow steps: cleaning, temperature-controlled sterilization and "
            "packaging.</p>"
        ),
        "how_fr": (
            "<h3>Comment fonctionnait la solution RFID ?</h3>"
            "<p>Le client a d’abord validé l’intégration de deux puces RFID dans chaque "
            "instrument afin qu’au moins une puce puisse être lue avec précision en conditions "
            "normales d’utilisation.</p>"
            "<p>OAAS a ensuite intégré des lecteurs RFID CAEN à la plateforme et modélisé les "
            "étapes successives du flux : nettoyage, stérilisation à température contrôlée et "
            "conditionnement.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A proof-of-concept platform combining CAEN readers, Raspberry Pi hardware, 4G "
            "connectivity and hosted software was created and operated between 2020 and "
            "2022.</p>"
            "<p>The solution demonstrated that RFID could capture the progress of instruments "
            "through the complete preparation and sterilization process.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Une plateforme de preuve de concept combinant lecteurs CAEN, matériel "
            "Raspberry Pi, connectivité 4G et logiciel hébergé a été créée et exploitée entre "
            "2020 et 2022.</p>"
            "<p>La solution a démontré que le RFID pouvait capturer la progression des "
            "instruments tout au long du processus complet de préparation et de "
            "stérilisation.</p>"
        ),
        "conclusion": (
            "<p>The platform gave the client a practical foundation for monitoring process "
            "quality in orthodontic practices.</p>"
            "<p>It also validated the technical choices required for mobile RFID reading and "
            "end-to-end sterilization traceability.</p>"
        ),
        "conclusion_fr": (
            "<p>La plateforme a offert au client une base concrète pour surveiller la qualité "
            "des processus dans les cabinets orthodontiques.</p>"
            "<p>Elle a également validé les choix techniques nécessaires à la lecture RFID "
            "mobile et à la traçabilité de la stérilisation de bout en bout.</p>"
        ),
        "summary": (
            "<p>Innovapeek explored how RFID could provide reliable traceability for "
            "orthodontic instruments throughout cleaning and sterilization. OAAS integrated "
            "readers, mobile connectivity and workflow software into a field-ready proof of "
            "concept.</p>"
        ),
        "summary_fr": (
            "<p>Innovapeek a exploré comment le RFID pouvait assurer une traçabilité fiable des "
            "instruments orthodontiques tout au long du nettoyage et de la stérilisation. OAAS "
            "a intégré lecteurs, connectivité mobile et logiciel de flux dans une preuve de "
            "concept prête pour le terrain.</p>"
        ),
        "adv_label": "End-to-end traceability",
        "adv_label_fr": "Traçabilité de bout en bout",
    },
    # 4 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Auditien: technical leadership and application continuity",
        "title_fr": "Auditien : leadership technique et continuité applicative",
        "subtitle": "A one-year CTO partnership for maintaining an auditory serious game",
        "subtitle_fr": "Un partenariat CTO d’un an pour maintenir un serious game auditif",
        "post_date": "12/02/2024 00:00:02",
        "meta_title": "Application Maintenance and CTO Support | Auditien",
        "meta_description": "OAAS supported Auditien for one year with application maintenance, bug fixing, project management and technical prioritization.",
        "meta_keywords": "CTO support, application maintenance, serious game, PHP, project management, bug fixing, OAAS",
        "meta_title_fr": "Maintenance applicative et accompagnement CTO | Auditien",
        "meta_description_fr": "OAAS a accompagné Auditien pendant un an avec de la maintenance applicative, de la correction de bugs, de la gestion de projet et de la priorisation technique.",
        "meta_keywords_fr": "accompagnement CTO, maintenance applicative, serious game, PHP, gestion de projet, correction de bugs, OAAS",
        "why": (
            "<h3>Why was technical continuity essential?</h3>"
            "<p>The departure of the original development team left the client with a live "
            "product but no internal capacity to maintain it.</p>"
            "<p>The priority was to preserve service continuity, understand the existing "
            "codebase and organize corrective work without exposing the platform to "
            "uncontrolled changes.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi la continuité technique était-elle essentielle ?</h3>"
            "<p>Le départ de l’équipe de développement initiale a laissé le client avec un "
            "produit en production mais sans capacité interne pour le maintenir.</p>"
            "<p>La priorité était de préserver la continuité de service, de comprendre la base "
            "de code existante et d’organiser le travail correctif sans exposer la plateforme à "
            "des changements incontrôlés.</p>"
        ),
        "how": (
            "<h3>How did OAAS support the platform?</h3>"
            "<p>OAAS took responsibility for technical follow-up, investigated incidents and "
            "corrected defects throughout the engagement.</p>"
            "<p>The work was managed through explicit risk and priority reviews so that urgent "
            "issues were handled first while longer-term improvements remained visible.</p>"
        ),
        "how_fr": (
            "<h3>Comment OAAS a-t-il accompagné la plateforme ?</h3>"
            "<p>OAAS a pris en charge le suivi technique, investigué les incidents et corrigé "
            "les défauts tout au long de la mission.</p>"
            "<p>Le travail a été piloté par des revues explicites de risques et de priorités, "
            "afin que les problèmes urgents soient traités en premier tout en gardant visibles "
            "les améliorations de plus long terme.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>The PHP serious-game platform was maintained for one year in 2018.</p>"
            "<p>The engagement combined hands-on maintenance with project management and "
            "CTO-level decision support.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>La plateforme de serious game en PHP a été maintenue pendant un an en 2018.</p>"
            "<p>La mission combinait maintenance opérationnelle, gestion de projet et aide à la "
            "décision au niveau CTO.</p>"
        ),
        "conclusion": (
            "<p>The partnership gave Auditien the technical continuity needed to keep its "
            "platform operational after a major team transition.</p>"
            "<p>It also restored a structured way to assess risks, prioritize work and make "
            "informed product decisions.</p>"
        ),
        "conclusion_fr": (
            "<p>Le partenariat a donné à Auditien la continuité technique nécessaire pour "
            "maintenir sa plateforme opérationnelle après une transition d’équipe majeure.</p>"
            "<p>Il a également rétabli une manière structurée d’évaluer les risques, de "
            "prioriser le travail et de prendre des décisions produit éclairées.</p>"
        ),
        "summary": (
            "<p>When Auditien's development team left, the company needed immediate technical "
            "continuity. OAAS provided a one-year CTO partnership to stabilize and maintain its "
            "auditory serious-game platform.</p>"
        ),
        "summary_fr": (
            "<p>Lorsque l’équipe de développement d’Auditien est partie, l’entreprise avait "
            "besoin d’une continuité technique immédiate. OAAS a fourni un partenariat CTO d’un "
            "an pour stabiliser et maintenir sa plateforme de serious game auditif.</p>"
        ),
        "adv_label": "Immediate continuity",
        "adv_label_fr": "Continuité immédiate",
    },
    # 5 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Fareva: a three-year LabWare LIMS transformation",
        "title_fr": "Fareva : une transformation LabWare LIMS sur trois ans",
        "subtitle": "Project management, specification and knowledge transfer for a pharmaceutical laboratory system",
        "subtitle_fr": "Gestion de projet, spécification et transfert de connaissances pour un système de laboratoire pharmaceutique",
        "post_date": "12/02/2024 00:00:03",
        "meta_title": "LabWare LIMS Project Management | Fareva & OAAS",
        "meta_description": "OAAS managed a three-year LabWare LIMS program covering deployment, system transfer, infrastructure, specifications, training and quality requirements.",
        "meta_keywords": "LabWare LIMS, pharmaceutical IT, LIMS migration, project management, Oracle migration, quality, training, OAAS",
        "meta_title_fr": "Gestion de projet LabWare LIMS | Fareva & OAAS",
        "meta_description_fr": "OAAS a piloté un programme LabWare LIMS de trois ans couvrant le déploiement, le transfert de système, l’infrastructure, les spécifications, la formation et les exigences qualité.",
        "meta_keywords_fr": "LabWare LIMS, informatique pharmaceutique, migration LIMS, gestion de projet, migration Oracle, qualité, formation, OAAS",
        "why": (
            "<h3>Why was a structured LIMS program required?</h3>"
            "<p>Laboratory information systems sit at the intersection of operations, quality, "
            "infrastructure and regulatory expectations. A successful deployment therefore "
            "requires more than software installation.</p>"
            "<p>The program had two distinct objectives: deploy the American LabWare LIMS in "
            "French sites, then transfer and rebuild the system for Fareva.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi un programme LIMS structuré était-il nécessaire ?</h3>"
            "<p>Les systèmes d’information de laboratoire se situent au croisement des "
            "opérations, de la qualité, de l’infrastructure et des exigences réglementaires. Un "
            "déploiement réussi demande donc bien plus qu’une simple installation logicielle.</p>"
            "<p>Le programme avait deux objectifs distincts : déployer le LIMS américain "
            "LabWare sur des sites français, puis transférer et reconstruire le système pour "
            "Fareva.</p>"
        ),
        "how": (
            "<h3>How was the transformation managed?</h3>"
            "<p>During the first phase, OAAS gathered requirements, identified gaps, "
            "coordinated hardware installation and local partners, managed budgets and prepared "
            "key-user training.</p>"
            "<p>The second phase required the existing MSD requirements to be rewritten for "
            "Fareva, the technical architecture to be reassessed and the team to be trained for "
            "autonomy.</p>"
        ),
        "how_fr": (
            "<h3>Comment la transformation a-t-elle été pilotée ?</h3>"
            "<p>Lors de la première phase, OAAS a recueilli les besoins, identifié les écarts, "
            "coordonné l’installation du matériel et les partenaires locaux, géré les budgets et "
            "préparé la formation des utilisateurs clés.</p>"
            "<p>La seconde phase a nécessité la réécriture des exigences MSD existantes pour "
            "Fareva, la réévaluation de l’architecture technique et la formation de l’équipe à "
            "l’autonomie.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>The three-year mission covered project management, LIMS specifications, "
            "infrastructure coordination, quality activities and team training.</p>"
            "<p>The client team was progressively trained so that it could operate and evolve "
            "the new environment autonomously.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>La mission de trois ans a couvert la gestion de projet, les spécifications "
            "LIMS, la coordination de l’infrastructure, les activités qualité et la formation "
            "des équipes.</p>"
            "<p>L’équipe client a été progressivement formée afin de pouvoir exploiter et faire "
            "évoluer le nouvel environnement de manière autonome.</p>"
        ),
        "conclusion": (
            "<p>The program created a controlled transition from an inherited LIMS environment "
            "to a system aligned with Fareva's own organization and constraints.</p>"
            "<p>Its long-term value came from combining delivery with documentation, training "
            "and operational autonomy.</p>"
        ),
        "conclusion_fr": (
            "<p>Le programme a créé une transition maîtrisée depuis un environnement LIMS "
            "hérité vers un système aligné sur l’organisation et les contraintes propres à "
            "Fareva.</p>"
            "<p>Sa valeur à long terme tient à la combinaison de la livraison avec la "
            "documentation, la formation et l’autonomie opérationnelle.</p>"
        ),
        "summary": (
            "<p>OAAS led a three-year LabWare LIMS program in a pharmaceutical environment. The "
            "mission covered an initial French deployment followed by the transfer and "
            "reconstruction of the system for Fareva.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a mené un programme LabWare LIMS de trois ans dans un environnement "
            "pharmaceutique. La mission a couvert un premier déploiement français, suivi du "
            "transfert et de la reconstruction du système pour Fareva.</p>"
        ),
        "adv_label": "Controlled system transition",
        "adv_label_fr": "Transition de système maîtrisée",
    },
    # 6 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Confidential project: real-time laboratory device integration",
        "title_fr": "Projet confidentiel : intégration d’un appareil de laboratoire en temps réel",
        "subtitle": "A specification-driven C# integration delivered under strict confidentiality",
        "subtitle_fr": "Une intégration C# pilotée par les spécifications, livrée sous stricte confidentialité",
        "post_date": "12/02/2024 00:00:04",
        "meta_title": "Real-Time Laboratory Device Integration | OAAS",
        "meta_description": "OAAS specified, developed and tested a confidential C# application integrating laboratory equipment into a real-time environment.",
        "meta_keywords": "laboratory device integration, real-time application, C#, specifications, testing, confidential project, OAAS",
        "meta_title_fr": "Intégration d’appareil de laboratoire en temps réel | OAAS",
        "meta_description_fr": "OAAS a spécifié, développé et testé une application C# confidentielle intégrant un équipement de laboratoire dans un environnement temps réel.",
        "meta_keywords_fr": "intégration d’appareil de laboratoire, application temps réel, C#, spécifications, tests, projet confidentiel, OAAS",
        "why": (
            "<h3>Why did the device need a real-time integration layer?</h3>"
            "<p>The client needed laboratory equipment to participate in a broader operational "
            "environment where data and actions had to be handled without manual delays.</p>"
            "<p>Because the project was confidential and technically sensitive, the expected "
            "behavior had to be described precisely before development.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi l’appareil avait-il besoin d’une couche d’intégration temps réel ?</h3>"
            "<p>Le client avait besoin que l’équipement de laboratoire participe à un "
            "environnement opérationnel plus large, où les données et les actions devaient être "
            "traitées sans délais manuels.</p>"
            "<p>Le projet étant confidentiel et techniquement sensible, le comportement attendu "
            "devait être décrit précisément avant le développement.</p>"
        ),
        "how": (
            "<h3>How was the integration secured?</h3>"
            "<p>OAAS studied the complete workflow and produced detailed specifications with "
            "the client.</p>"
            "<p>Once both parties had validated the expected behavior, the device integration "
            "was developed and tested through several controlled phases, focusing on "
            "predictable communication between systems.</p>"
        ),
        "how_fr": (
            "<h3>Comment l’intégration a-t-elle été sécurisée ?</h3>"
            "<p>OAAS a étudié le flux complet et produit des spécifications détaillées avec le "
            "client.</p>"
            "<p>Une fois le comportement attendu validé par les deux parties, l’intégration de "
            "l’appareil a été développée et testée à travers plusieurs phases contrôlées, en se "
            "concentrant sur une communication prévisible entre les systèmes.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A C# application was delivered on schedule and transferred to the client.</p>"
            "<p>The resulting solution was integrated into the client's commercial offering.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Une application C# a été livrée dans les délais et transférée au client.</p>"
            "<p>La solution obtenue a été intégrée à l’offre commerciale du client.</p>"
        ),
        "conclusion": (
            "<p>The project demonstrated that a sensitive device integration can be delivered "
            "efficiently when specifications and acceptance tests are treated as core "
            "engineering work.</p>"
            "<p>Confidentiality limits the detail that can be shared, but the delivered "
            "solution met both the technical and commercial objectives.</p>"
        ),
        "conclusion_fr": (
            "<p>Le projet a démontré qu’une intégration d’appareil sensible peut être livrée "
            "efficacement lorsque les spécifications et les tests de recette sont traités comme "
            "un travail d’ingénierie à part entière.</p>"
            "<p>La confidentialité limite le niveau de détail partageable, mais la solution "
            "livrée a atteint les objectifs techniques comme commerciaux.</p>"
        ),
        "summary": (
            "<p>OAAS integrated a laboratory device into a real-time software environment for a "
            "confidential client. The work emphasized jointly validated specifications, "
            "controlled testing and reliable delivery.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a intégré un appareil de laboratoire dans un environnement logiciel temps "
            "réel pour un client confidentiel. Le travail a mis l’accent sur des spécifications "
            "validées conjointement, des tests maîtrisés et une livraison fiable.</p>"
        ),
        "adv_label": "Validated specifications",
        "adv_label_fr": "Spécifications validées",
    },
    # 7 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Infogene: food traceability specifications for Qatar",
        "title_fr": "Infogene : spécifications de traçabilité alimentaire pour le Qatar",
        "subtitle": "A consulting mission mapping the food chain before the Football World Cup",
        "subtitle_fr": "Une mission de conseil cartographiant la chaîne alimentaire avant la Coupe du Monde de football",
        "post_date": "12/02/2024 00:00:05",
        "meta_title": "Food Traceability Consulting and Specifications | OAAS",
        "meta_description": "OAAS contributed to food traceability specifications for Qatar using SIPOC, RACI and value-stream mapping across the supply chain.",
        "meta_keywords": "food traceability, Qatar, specifications, SIPOC, RACI, value stream mapping, LIMS, OAAS",
        "meta_title_fr": "Conseil et spécifications en traçabilité alimentaire | OAAS",
        "meta_description_fr": "OAAS a contribué aux spécifications de traçabilité alimentaire pour le Qatar à l’aide de SIPOC, RACI et de la cartographie de la chaîne de valeur sur l’ensemble de la chaîne d’approvisionnement.",
        "meta_keywords_fr": "traçabilité alimentaire, Qatar, spécifications, SIPOC, RACI, cartographie de la chaîne de valeur, LIMS, OAAS",
        "why": (
            "<h3>Why define traceability before building the system?</h3>"
            "<p>A national food-traceability system must connect many organizations, processes "
            "and control points. If responsibilities and data exchanges are unclear, software "
            "alone cannot provide reliable oversight.</p>"
            "<p>The first objective was therefore to document the complete chain and establish "
            "specifications that everyone could rely on.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi définir la traçabilité avant de construire le système ?</h3>"
            "<p>Un système national de traçabilité alimentaire doit relier de nombreuses "
            "organisations, processus et points de contrôle. Si les responsabilités et les "
            "échanges de données sont flous, le logiciel seul ne peut pas assurer un suivi "
            "fiable.</p>"
            "<p>Le premier objectif était donc de documenter la chaîne complète et d’établir "
            "des spécifications sur lesquelles chacun pouvait s’appuyer.</p>"
        ),
        "how": (
            "<h3>How was the food chain analyzed?</h3>"
            "<p>The consulting team used SIPOC to identify suppliers, inputs, processes, "
            "outputs and customers across the chain.</p>"
            "<p>RACI analysis clarified who was responsible, accountable, consulted and "
            "informed at each stage, while value-stream mapping helped expose the operational "
            "flow from border controls to delivery.</p>"
        ),
        "how_fr": (
            "<h3>Comment la chaîne alimentaire a-t-elle été analysée ?</h3>"
            "<p>L’équipe de conseil a utilisé SIPOC pour identifier fournisseurs, entrants, "
            "processus, sortants et clients tout au long de la chaîne.</p>"
            "<p>L’analyse RACI a clarifié qui était responsable, garant, consulté et informé à "
            "chaque étape, tandis que la cartographie de la chaîne de valeur a permis "
            "d’exposer le flux opérationnel des contrôles aux frontières jusqu’à la "
            "livraison.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A complete set of food-traceability specifications was produced and handed over "
            "for review by another team.</p>"
            "<p>The work provided a structured foundation that supported the creation of the "
            "client's own laboratory information and traceability environment.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Un ensemble complet de spécifications de traçabilité alimentaire a été produit "
            "et remis pour relecture par une autre équipe.</p>"
            "<p>Le travail a fourni une base structurée qui a soutenu la création de "
            "l’environnement d’information de laboratoire et de traçabilité propre au client.</p>"
        ),
        "conclusion": (
            "<p>The mission showed the value of process modeling before technology "
            "selection.</p>"
            "<p>By making flows and responsibilities explicit, the specifications reduced "
            "ambiguity and gave implementation teams a shared reference.</p>"
        ),
        "conclusion_fr": (
            "<p>La mission a montré l’intérêt de modéliser les processus avant de choisir la "
            "technologie.</p>"
            "<p>En rendant explicites les flux et les responsabilités, les spécifications ont "
            "réduit l’ambiguïté et donné aux équipes de mise en œuvre une référence "
            "commune.</p>"
        ),
        "summary": (
            "<p>OAAS joined a three-person consulting team to define food-traceability "
            "requirements for Qatar before the Football World Cup. The mission mapped "
            "responsibilities and information flows from border entry to final delivery.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a rejoint une équipe de conseil de trois personnes pour définir les "
            "exigences de traçabilité alimentaire du Qatar avant la Coupe du Monde de football. "
            "La mission a cartographié les responsabilités et les flux d’information de l’entrée "
            "aux frontières jusqu’à la livraison finale.</p>"
        ),
        "adv_label": "Complete supply-chain view",
        "adv_label_fr": "Vision complète de la chaîne d’approvisionnement",
    },
    # 8 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Nocash: an early contactless payment platform for bars",
        "title_fr": "Nocash : une plateforme de paiement sans contact précoce pour les bars",
        "subtitle": "RFID wristbands, a cross-platform mobile application and a secure Python backend",
        "subtitle_fr": "Des bracelets RFID, une application mobile multiplateforme et un backend Python sécurisé",
        "post_date": "12/02/2024 00:00:06",
        "meta_title": "RFID Contactless Payment Platform for Bars | Nocash",
        "meta_description": "Nocash created an RFID wristband payment solution for bars, combining a cross-platform mobile application with a secure Python and Django backend.",
        "meta_keywords": "contactless payment, RFID wristband, bars, Xamarin, C#, Python, Django, secure hosting, OAAS",
        "meta_title_fr": "Plateforme de paiement sans contact RFID pour bars | Nocash",
        "meta_description_fr": "Nocash a créé une solution de paiement par bracelet RFID pour les bars, combinant une application mobile multiplateforme et un backend Python et Django sécurisé.",
        "meta_keywords_fr": "paiement sans contact, bracelet RFID, bars, Xamarin, C#, Python, Django, hébergement sécurisé, OAAS",
        "why": (
            "<h3>Why create a dedicated contactless payment experience?</h3>"
            "<p>Bars needed a faster way to handle purchases and reduce friction at busy "
            "service points. At the time, consumer phones did not yet provide today's common "
            "contactless-payment capabilities.</p>"
            "<p>RFID wristbands offered a practical alternative that could connect each customer "
            "to a secure balance and speed up transactions.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi créer une expérience de paiement sans contact dédiée ?</h3>"
            "<p>Les bars avaient besoin d’un moyen plus rapide de gérer les achats et de "
            "réduire les frictions aux points de service chargés. À l’époque, les téléphones "
            "grand public n’offraient pas encore les capacités de paiement sans contact "
            "aujourd’hui courantes.</p>"
            "<p>Les bracelets RFID offraient une alternative pratique, capable de relier chaque "
            "client à un solde sécurisé et d’accélérer les transactions.</p>"
        ),
        "how": (
            "<h3>How was the solution developed?</h3>"
            "<p>The team created the company and managed a constrained development budget "
            "covering product design, software, hosting and wristband production.</p>"
            "<p>RFID wristbands and related goods were manufactured in China. A cross-platform "
            "mobile application was developed with C# and Xamarin, while the backend used "
            "Python and Django.</p>"
        ),
        "how_fr": (
            "<h3>Comment la solution a-t-elle été développée ?</h3>"
            "<p>L’équipe a créé l’entreprise et géré un budget de développement contraint "
            "couvrant le design produit, le logiciel, l’hébergement et la production des "
            "bracelets.</p>"
            "<p>Les bracelets RFID et produits associés ont été fabriqués en Chine. Une "
            "application mobile multiplateforme a été développée avec C# et Xamarin, tandis que "
            "le backend utilisait Python et Django.</p>"
        ),
        "what": (
            "<h3>What was achieved?</h3>"
            "<p>The payment platform operated during 2020 and 2021 and reached an initial "
            "field-testing stage.</p>"
            "<p>The project was ultimately stopped after the prolonged impact of the COVID-19 "
            "crisis on the hospitality sector.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été accompli ?</h3>"
            "<p>La plateforme de paiement a fonctionné en 2020 et 2021 et a atteint une "
            "première phase de test terrain.</p>"
            "<p>Le projet a finalement été arrêté après l’impact prolongé de la crise du "
            "COVID-19 sur le secteur de l’hôtellerie-restauration.</p>"
        ),
        "conclusion": (
            "<p>Nocash validated a complete contactless-payment concept before mobile "
            "contactless capabilities became mainstream.</p>"
            "<p>Although market conditions prevented commercial continuation, the project "
            "demonstrated OAAS's ability to deliver hardware-connected payments, mobile "
            "software and secure backend infrastructure as one product.</p>"
        ),
        "conclusion_fr": (
            "<p>Nocash a validé un concept complet de paiement sans contact avant que les "
            "capacités mobiles sans contact ne se généralisent.</p>"
            "<p>Bien que les conditions de marché aient empêché une suite commerciale, le "
            "projet a démontré la capacité d’OAAS à livrer en un seul produit des paiements "
            "connectés au matériel, un logiciel mobile et une infrastructure backend "
            "sécurisée.</p>"
        ),
        "summary": (
            "<p>Before contactless mobile payments became widespread, Nocash developed an RFID "
            "wristband payment solution for bars. The project covered hardware sourcing, mobile "
            "development, backend services, hosting and real-world trials.</p>"
        ),
        "summary_fr": (
            "<p>Avant que les paiements mobiles sans contact ne se généralisent, Nocash a "
            "développé une solution de paiement par bracelet RFID pour les bars. Le projet a "
            "couvert l’approvisionnement matériel, le développement mobile, les services "
            "backend, l’hébergement et les essais en conditions réelles.</p>"
        ),
        "adv_label": "Faster bar transactions",
        "adv_label_fr": "Transactions plus rapides au bar",
    },
    # 9 ----------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Scierie du Forez: automating forest parcel valuation in Excel",
        "title_fr": "Scierie du Forez : automatiser la valorisation des parcelles forestières dans Excel",
        "subtitle": "A practical tool for estimating timber volume and parcel value",
        "subtitle_fr": "Un outil concret pour estimer le volume de bois et la valeur des parcelles",
        "post_date": "12/02/2024 00:00:07",
        "meta_title": "Excel Automation for Forest Parcel Valuation | OAAS",
        "meta_description": "OAAS automated an Excel tool used by Scierie du Forez to calculate timber volumes and estimate the value of forest parcels.",
        "meta_keywords": "Excel automation, forestry, timber volume, forest parcel valuation, SME digitalization, OAAS",
        "meta_title_fr": "Automatisation Excel pour la valorisation de parcelles forestières | OAAS",
        "meta_description_fr": "OAAS a automatisé un outil Excel utilisé par la Scierie du Forez pour calculer les volumes de bois et estimer la valeur des parcelles forestières.",
        "meta_keywords_fr": "automatisation Excel, sylviculture, volume de bois, valorisation de parcelles forestières, digitalisation PME, OAAS",
        "why": (
            "<h3>Why automate a small but critical business process?</h3>"
            "<p>The client already knew how to calculate the volume of wood contained in a "
            "forest parcel, but the manual process was time-consuming and difficult to repeat "
            "consistently.</p>"
            "<p>A lightweight Excel solution was the appropriate choice because it matched "
            "existing working habits while removing repetitive manual steps.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi automatiser un processus métier modeste mais critique ?</h3>"
            "<p>Le client savait déjà calculer le volume de bois contenu dans une parcelle "
            "forestière, mais le processus manuel était chronophage et difficile à reproduire "
            "de manière cohérente.</p>"
            "<p>Une solution Excel légère était le choix approprié, car elle correspondait aux "
            "habitudes de travail existantes tout en supprimant les étapes manuelles "
            "répétitives.</p>"
        ),
        "how": (
            "<h3>How was the workbook automated?</h3>"
            "<p>The customer supplied the algorithms and worked with OAAS to define the "
            "complete functional specifications.</p>"
            "<p>OAAS then structured and automated the workbook so that users could enter "
            "parcel information and obtain consistent volume and price estimates, focusing on "
            "clarity and reliability.</p>"
        ),
        "how_fr": (
            "<h3>Comment le classeur a-t-il été automatisé ?</h3>"
            "<p>Le client a fourni les algorithmes et travaillé avec OAAS pour définir les "
            "spécifications fonctionnelles complètes.</p>"
            "<p>OAAS a ensuite structuré et automatisé le classeur afin que les utilisateurs "
            "puissent saisir les informations de parcelle et obtenir des estimations cohérentes "
            "de volume et de prix, en privilégiant la clarté et la fiabilité.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>An automated Excel workbook used to estimate the value of forest parcels.</p>"
            "<p>The tool has remained in production for five years, demonstrating the value of "
            "a focused solution aligned with the actual workflow.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Un classeur Excel automatisé servant à estimer la valeur des parcelles "
            "forestières.</p>"
            "<p>L’outil est resté en production pendant cinq ans, démontrant la valeur d’une "
            "solution ciblée alignée sur le flux de travail réel.</p>"
        ),
        "conclusion": (
            "<p>This project is a practical example of digitalization at the right scale.</p>"
            "<p>By automating an existing expert method instead of replacing it with a large "
            "application, OAAS delivered immediate value with minimal disruption.</p>"
        ),
        "conclusion_fr": (
            "<p>Ce projet est un exemple concret de digitalisation à la bonne échelle.</p>"
            "<p>En automatisant une méthode experte existante au lieu de la remplacer par une "
            "grande application, OAAS a apporté une valeur immédiate avec un minimum de "
            "perturbation.</p>"
        ),
        "summary": (
            "<p>OAAS helped Scierie du Forez turn an expert calculation method into an "
            "automated Excel tool for estimating timber volume and forest-parcel value.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a aidé la Scierie du Forez à transformer une méthode de calcul experte en "
            "un outil Excel automatisé pour estimer le volume de bois et la valeur des "
            "parcelles forestières.</p>"
        ),
        "adv_label": "Time saved on calculations",
        "adv_label_fr": "Temps gagné sur les calculs",
    },
    # 10 ---------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Telecom ParisTech: visualizing and teaching the 4G protocol",
        "title_fr": "Télécom ParisTech : visualiser et enseigner le protocole 4G",
        "subtitle": "An educational data platform for acquiring, parsing and displaying 4G frames",
        "subtitle_fr": "Une plateforme de données pédagogique pour acquérir, analyser et afficher les trames 4G",
        "post_date": "31/07/2024 00:00:08",
        "meta_title": "4G Protocol Analysis and Visualization Platform | OAAS",
        "meta_description": "OAAS helped Telecom ParisTech create an educational platform that acquires, parses and visualizes 4G protocol frames.",
        "meta_keywords": "4G protocol, telecom education, protocol analysis, data visualization, frame parsing, data platform, OAAS",
        "meta_title_fr": "Plateforme d’analyse et de visualisation du protocole 4G | OAAS",
        "meta_description_fr": "OAAS a aidé Télécom ParisTech à créer une plateforme pédagogique qui acquiert, analyse et visualise les trames du protocole 4G.",
        "meta_keywords_fr": "protocole 4G, enseignement télécom, analyse de protocole, visualisation de données, analyse de trames, plateforme de données, OAAS",
        "why": (
            "<h3>Why visualize a complex communication protocol?</h3>"
            "<p>The 4G protocol contains many interacting paths and message exchanges that are "
            "difficult to understand from specifications alone.</p>"
            "<p>An educational platform could make these exchanges visible and give students a "
            "concrete way to investigate how the protocol behaves.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi visualiser un protocole de communication complexe ?</h3>"
            "<p>Le protocole 4G contient de nombreux chemins et échanges de messages qui "
            "interagissent et sont difficiles à comprendre à partir des seules "
            "spécifications.</p>"
            "<p>Une plateforme pédagogique pouvait rendre ces échanges visibles et offrir aux "
            "étudiants un moyen concret d’explorer le comportement du protocole.</p>"
        ),
        "how": (
            "<h3>How was the platform created?</h3>"
            "<p>The partnership began with knowledge transfer to understand the key protocol "
            "paths and identify the information that would be most useful for teaching.</p>"
            "<p>The team then used 4G protocol-analysis tools to validate the theoretical model "
            "against real frames, and finally created the data pipeline required to acquire, "
            "parse and display them.</p>"
        ),
        "how_fr": (
            "<h3>Comment la plateforme a-t-elle été créée ?</h3>"
            "<p>Le partenariat a commencé par un transfert de connaissances pour comprendre les "
            "principaux chemins du protocole et identifier les informations les plus utiles à "
            "l’enseignement.</p>"
            "<p>L’équipe a ensuite utilisé des outils d’analyse du protocole 4G pour valider le "
            "modèle théorique face à des trames réelles, puis a créé le pipeline de données "
            "nécessaire pour les acquérir, les analyser et les afficher.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>The application was completed within a few months and transferred to Telecom "
            "ParisTech.</p>"
            "<p>It provided an educational tool that combined protocol acquisition, structured "
            "parsing and visual exploration.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>L’application a été réalisée en quelques mois et transférée à Télécom "
            "ParisTech.</p>"
            "<p>Elle a fourni un outil pédagogique combinant acquisition du protocole, analyse "
            "structurée et exploration visuelle.</p>"
        ),
        "conclusion": (
            "<p>The project strengthened OAAS's understanding of communication protocols and "
            "their practical integration.</p>"
            "<p>That expertise is directly relevant to connected devices, where reliable "
            "protocol handling is a core part of IoT engineering.</p>"
        ),
        "conclusion_fr": (
            "<p>Le projet a renforcé la maîtrise par OAAS des protocoles de communication et de "
            "leur intégration pratique.</p>"
            "<p>Cette expertise est directement pertinente pour les appareils connectés, où un "
            "traitement fiable des protocoles est un élément central de l’ingénierie IoT.</p>"
        ),
        "summary": (
            "<p>OAAS partnered with Telecom ParisTech to create an educational platform for "
            "understanding the 4G protocol. The application acquires, parses and visualizes "
            "protocol frames so learners can connect theory with real communication flows.</p>"
        ),
        "summary_fr": (
            "<p>OAAS s’est associé à Télécom ParisTech pour créer une plateforme pédagogique "
            "permettant de comprendre le protocole 4G. L’application acquiert, analyse et "
            "visualise les trames du protocole afin que les apprenants relient la théorie aux "
            "flux de communication réels.</p>"
        ),
        "adv_label": "Theory connected to real data",
        "adv_label_fr": "Théorie reliée aux données réelles",
    },
    # 11 ---------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "Confidential project: a secure insurance data platform",
        "title_fr": "Projet confidentiel : une plateforme de données d’assurance sécurisée",
        "subtitle": "A complete analytics environment delivered within a short timeframe",
        "subtitle_fr": "Un environnement d’analyse complet livré dans un délai court",
        "post_date": "31/07/2024 00:00:08",
        "meta_title": "Secure Insurance Data Platform | OAAS",
        "meta_description": "OAAS delivered a confidential insurance data-analysis platform after a focused specification, development and testing process.",
        "meta_keywords": "insurance data platform, data analysis, secure hosting, specifications, testing, confidential project, OAAS",
        "meta_title_fr": "Plateforme de données d’assurance sécurisée | OAAS",
        "meta_description_fr": "OAAS a livré une plateforme d’analyse de données d’assurance confidentielle après un processus ciblé de spécification, de développement et de tests.",
        "meta_keywords_fr": "plateforme de données d’assurance, analyse de données, hébergement sécurisé, spécifications, tests, projet confidentiel, OAAS",
        "why": (
            "<h3>Why was a dedicated data platform needed?</h3>"
            "<p>Insurance analysis depends on consolidating data into a controlled environment "
            "where teams can explore information consistently and securely.</p>"
            "<p>The client needed a complete platform quickly, making scope clarity and "
            "delivery discipline essential from the start.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi une plateforme de données dédiée était-elle nécessaire ?</h3>"
            "<p>L’analyse en assurance repose sur la consolidation des données dans un "
            "environnement contrôlé où les équipes peuvent explorer l’information de manière "
            "cohérente et sécurisée.</p>"
            "<p>Le client avait besoin d’une plateforme complète rapidement, ce qui rendait "
            "essentielles dès le départ la clarté du périmètre et la discipline de "
            "livraison.</p>"
        ),
        "how": (
            "<h3>How was rapid delivery made possible?</h3>"
            "<p>The project began with a focused specification phase that established the "
            "required workflows and expected results.</p>"
            "<p>OAAS then developed the platform in close cooperation with the client's team "
            "and validated it through multiple testing phases. Frequent feedback limited "
            "misunderstandings and allowed fast progress.</p>"
        ),
        "how_fr": (
            "<h3>Comment une livraison rapide a-t-elle été possible ?</h3>"
            "<p>Le projet a commencé par une phase de spécification ciblée qui a établi les "
            "flux requis et les résultats attendus.</p>"
            "<p>OAAS a ensuite développé la plateforme en coopération étroite avec l’équipe du "
            "client et l’a validée à travers plusieurs phases de test. Des retours fréquents "
            "ont limité les malentendus et permis une progression rapide.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A complete insurance data-analysis application hosted by OAAS.</p>"
            "<p>The production environment was designed with a high level of security "
            "appropriate for sensitive business data.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Une application complète d’analyse de données d’assurance hébergée par OAAS.</p>"
            "<p>L’environnement de production a été conçu avec un haut niveau de sécurité "
            "adapté à des données métier sensibles.</p>"
        ),
        "conclusion": (
            "<p>The project demonstrates how strong specifications and an engaged client team "
            "can accelerate delivery.</p>"
            "<p>Despite confidentiality constraints, the outcome combined rapid implementation, "
            "structured testing and secure hosting.</p>"
        ),
        "conclusion_fr": (
            "<p>Le projet montre comment des spécifications solides et une équipe client "
            "engagée peuvent accélérer la livraison.</p>"
            "<p>Malgré les contraintes de confidentialité, le résultat a combiné une mise en "
            "œuvre rapide, des tests structurés et un hébergement sécurisé.</p>"
        ),
        "summary": (
            "<p>OAAS delivered a complete insurance data-analysis platform for a confidential "
            "client within a short timeframe. Strong specifications and close collaboration "
            "with the client's team kept delivery focused and testable.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a livré une plateforme complète d’analyse de données d’assurance pour un "
            "client confidentiel dans un délai court. Des spécifications solides et une "
            "collaboration étroite avec l’équipe du client ont gardé la livraison ciblée et "
            "testable.</p>"
        ),
        "adv_label": "Short delivery cycle",
        "adv_label_fr": "Cycle de livraison court",
    },
    # 12 ---------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "RDI Manager: rebuilding for high availability and replication",
        "title_fr": "RDI Manager : reconstruire pour la haute disponibilité et la réplication",
        "subtitle": "A documented infrastructure redesign for a secure business application",
        "subtitle_fr": "Une refonte d’infrastructure documentée pour une application métier sécurisée",
        "post_date": "31/07/2024 00:00:08",
        "meta_title": "High-Availability Infrastructure Rebuild | RDI Manager",
        "meta_description": "OAAS rebuilt and documented RDI Manager's infrastructure for high availability, replication and secure hosting.",
        "meta_keywords": "high availability, replicated infrastructure, application rebuild, secure hosting, documentation, RDI Manager, OAAS",
        "meta_title_fr": "Reconstruction d’infrastructure haute disponibilité | RDI Manager",
        "meta_description_fr": "OAAS a reconstruit et documenté l’infrastructure de RDI Manager pour la haute disponibilité, la réplication et un hébergement sécurisé.",
        "meta_keywords_fr": "haute disponibilité, infrastructure répliquée, reconstruction applicative, hébergement sécurisé, documentation, RDI Manager, OAAS",
        "why": (
            "<h3>Why rebuild the infrastructure?</h3>"
            "<p>The existing environment needed stronger availability and resilience, but "
            "limited documentation made safe evolution difficult.</p>"
            "<p>The objective was to create a cleaner, reproducible foundation that could be "
            "understood, tested and operated over time.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi reconstruire l’infrastructure ?</h3>"
            "<p>L’environnement existant avait besoin d’une disponibilité et d’une résilience "
            "renforcées, mais une documentation limitée rendait son évolution sereine "
            "difficile.</p>"
            "<p>L’objectif était de créer une base plus propre et reproductible, pouvant être "
            "comprise, testée et exploitée dans la durée.</p>"
        ),
        "how": (
            "<h3>How was the new environment secured?</h3>"
            "<p>OAAS first studied the existing application and infrastructure to identify "
            "dependencies and missing knowledge.</p>"
            "<p>A new implementation branch was then created with a higher level of technical "
            "documentation, and the OAAS and client teams carried out extensive testing "
            "together to validate behavior before the switch.</p>"
        ),
        "how_fr": (
            "<h3>Comment le nouvel environnement a-t-il été sécurisé ?</h3>"
            "<p>OAAS a d’abord étudié l’application et l’infrastructure existantes pour "
            "identifier les dépendances et les connaissances manquantes.</p>"
            "<p>Une nouvelle branche d’implémentation a ensuite été créée avec un niveau plus "
            "élevé de documentation technique, et les équipes OAAS et client ont mené ensemble "
            "des tests approfondis pour valider le comportement avant la bascule.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A rebuilt application environment designed for high availability and "
            "replication.</p>"
            "<p>The application is hosted by OAAS in a highly secured infrastructure.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Un environnement applicatif reconstruit, conçu pour la haute disponibilité et "
            "la réplication.</p>"
            "<p>L’application est hébergée par OAAS dans une infrastructure hautement "
            "sécurisée.</p>"
        ),
        "conclusion": (
            "<p>The rebuild reduced operational risk by combining technical resilience with "
            "maintainable documentation.</p>"
            "<p>It also gave both teams a clearer baseline for testing, support and future "
            "evolution.</p>"
        ),
        "conclusion_fr": (
            "<p>La reconstruction a réduit le risque opérationnel en combinant résilience "
            "technique et documentation maintenable.</p>"
            "<p>Elle a également donné aux deux équipes une référence plus claire pour les "
            "tests, le support et l’évolution future.</p>"
        ),
        "summary": (
            "<p>OAAS rebuilt RDI Manager's application environment to provide stronger "
            "availability, replication and documentation. The project combined infrastructure "
            "analysis, a clean implementation branch and extensive joint testing.</p>"
        ),
        "summary_fr": (
            "<p>OAAS a reconstruit l’environnement applicatif de RDI Manager pour offrir une "
            "meilleure disponibilité, une réplication et une documentation renforcées. Le "
            "projet a combiné analyse d’infrastructure, branche d’implémentation propre et "
            "tests conjoints approfondis.</p>"
        ),
        "adv_label": "Higher service resilience",
        "adv_label_fr": "Résilience de service accrue",
    },
    # 13 ---------------------------------------------------------------------
    {
        "blog": "Customers",
        "title": "IA-Aqua: a programmable IoT platform for farm automation",
        "title_fr": "IA-Aqua : une plateforme IoT programmable pour l’automatisation agricole",
        "subtitle": "A fresh, secure data environment connecting field devices and farming workflows",
        "subtitle_fr": "Un environnement de données neuf et sécurisé reliant appareils de terrain et flux agricoles",
        "post_date": "31/07/2024 00:00:08",
        "meta_title": "IoT Data Platform for Farming Automation | IA-Aqua",
        "meta_description": "OAAS delivered IA-Aqua's programmable IoT data platform in eight weeks, restoring device data and supporting flexible farm automation.",
        "meta_keywords": "farming automation, agriculture IoT, programmable IoT platform, device data, secure hosting, IA-Aqua, OAAS",
        "meta_title_fr": "Plateforme de données IoT pour l’automatisation agricole | IA-Aqua",
        "meta_description_fr": "OAAS a livré la plateforme de données IoT programmable d’IA-Aqua en huit semaines, restaurant les données des appareils et soutenant une automatisation agricole flexible.",
        "meta_keywords_fr": "automatisation agricole, IoT agricole, plateforme IoT programmable, données d’appareils, hébergement sécurisé, IA-Aqua, OAAS",
        "why": (
            "<h3>Why replace the existing IoT environment?</h3>"
            "<p>The previous platform was no longer maintained, creating risk around field "
            "data, connected devices and future development.</p>"
            "<p>The client operated many IoT devices and needed a flexible foundation that "
            "could support different farming use cases rather than another rigid, "
            "project-specific tool.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi remplacer l’environnement IoT existant ?</h3>"
            "<p>La plateforme précédente n’était plus maintenue, créant un risque autour des "
            "données de terrain, des appareils connectés et des développements futurs.</p>"
            "<p>Le client exploitait de nombreux appareils IoT et avait besoin d’une base "
            "flexible capable de supporter différents cas d’usage agricoles plutôt qu’un autre "
            "outil rigide et spécifique à un projet.</p>"
        ),
        "how": (
            "<h3>How was the new platform delivered?</h3>"
            "<p>The client provided detailed specifications while OAAS helped challenge usage "
            "scenarios, refine priorities and recover the required data.</p>"
            "<p>OAAS used its experience with IoT protocols and platforms to build a fresh "
            "programmable environment suited to the existing device fleet, with close "
            "collaboration throughout.</p>"
        ),
        "how_fr": (
            "<h3>Comment la nouvelle plateforme a-t-elle été livrée ?</h3>"
            "<p>Le client a fourni des spécifications détaillées tandis qu’OAAS a aidé à "
            "challenger les scénarios d’usage, affiner les priorités et récupérer les données "
            "nécessaires.</p>"
            "<p>OAAS a mis à profit son expérience des protocoles et plateformes IoT pour bâtir "
            "un environnement programmable neuf, adapté au parc d’appareils existant, avec une "
            "collaboration étroite tout au long du projet.</p>"
        ),
        "what": (
            "<h3>What was delivered?</h3>"
            "<p>A programmable IoT data platform supporting the client's farm-automation "
            "requirements and connected devices.</p>"
            "<p>The application is hosted by OAAS in a highly secured environment.</p>"
        ),
        "what_fr": (
            "<h3>Qu’est-ce qui a été livré ?</h3>"
            "<p>Une plateforme de données IoT programmable répondant aux besoins "
            "d’automatisation agricole du client et à ses appareils connectés.</p>"
            "<p>L’application est hébergée par OAAS dans un environnement hautement "
            "sécurisé.</p>"
        ),
        "conclusion": (
            "<p>The project restored a maintainable technical foundation while preserving the "
            "flexibility required for future agricultural use cases.</p>"
            "<p>Its eight-week delivery was enabled by clear specifications, shared domain "
            "knowledge and disciplined testing.</p>"
        ),
        "conclusion_fr": (
            "<p>Le projet a rétabli une base technique maintenable tout en préservant la "
            "flexibilité nécessaire aux futurs cas d’usage agricoles.</p>"
            "<p>Sa livraison en huit semaines a été rendue possible par des spécifications "
            "claires, une connaissance métier partagée et des tests rigoureux.</p>"
        ),
        "summary": (
            "<p>IA-Aqua needed to replace an unmaintained IoT environment without losing access "
            "to field data or flexibility. OAAS delivered a fresh programmable platform in "
            "eight weeks and validated it through a complete testing phase.</p>"
        ),
        "summary_fr": (
            "<p>IA-Aqua devait remplacer un environnement IoT non maintenu sans perdre l’accès "
            "aux données de terrain ni la flexibilité. OAAS a livré une plateforme programmable "
            "neuve en huit semaines et l’a validée à travers une phase de test complète.</p>"
        ),
        "adv_label": "Maintainable foundation",
        "adv_label_fr": "Base maintenable",
    },
    # 14 ---------------------------------------------------------------------
    {
        "blog": "Methods",
        "title": "SIPOC, RACI and VSM: maximizing process efficiency",
        "title_fr": "SIPOC, RACI et VSM : maximiser l’efficacité des processus",
        "subtitle": "Combining process mapping, role matrices and value-stream analysis to clarify and optimize how work flows",
        "subtitle_fr": "Combiner cartographie des processus, matrice des rôles et analyse de la chaîne de valeur pour clarifier et optimiser les flux de travail",
        "post_date": "31/07/2024 00:00:09",
        "meta_title": "SIPOC, RACI & VSM Process Methods | OAAS",
        "meta_title_fr": "Méthodes SIPOC, RACI & VSM pour vos processus | OAAS",
        "meta_description": "How OAAS uses SIPOC, the RACI matrix and value-stream mapping (VSM) to clarify workflows, define responsibilities and remove bottlenecks across complex processes.",
        "meta_description_fr": "Comment OAAS utilise SIPOC, la matrice RACI et la cartographie de la chaîne de valeur (VSM) pour clarifier les flux, définir les responsabilités et éliminer les goulets d’étranglement des processus complexes.",
        "meta_keywords": "SIPOC, RACI, VSM, value stream mapping, process mapping, process optimization, roles and responsibilities, lean, OAAS",
        "meta_keywords_fr": "SIPOC, RACI, VSM, cartographie de la chaîne de valeur, cartographie des processus, optimisation des processus, rôles et responsabilités, lean, OAAS",
        "why": (
            "<h3>Why combine SIPOC, RACI and VSM?</h3>"
            "<p>Organizations rarely struggle because their teams lack effort. They struggle "
            "because their <strong>processes are unclear</strong>: who does what, where the "
            "inputs come from, and where value is actually created often stays implicit.</p>"
            "<p>SIPOC (Suppliers, Inputs, Process, Outputs, Customers) gives a shared, "
            "high-level view of a workflow. The RACI matrix (Responsible, Accountable, "
            "Consulted, Informed) removes ambiguity about roles at each step. Value-stream "
            "mapping (VSM) exposes where time and value are lost.</p>"
            "<p>Used together, these methods turn a vague, interconnected process into "
            "something visible, owned and measurable - the prerequisite for any real "
            "improvement.</p>"
        ),
        "why_fr": (
            "<h3>Pourquoi combiner SIPOC, RACI et VSM ?</h3>"
            "<p>Les organisations échouent rarement par manque d’efforts. Elles échouent parce "
            "que leurs <strong>processus sont flous</strong> : qui fait quoi, d’où viennent les "
            "entrées et où la valeur est réellement créée reste souvent implicite.</p>"
            "<p>SIPOC (Fournisseurs, Entrées, Processus, Sorties, Clients) offre une vue "
            "d’ensemble partagée d’un flux de travail. La matrice RACI (Responsable, "
            "Approbateur, Consulté, Informé) lève l’ambiguïté sur les rôles à chaque étape. La "
            "cartographie de la chaîne de valeur (VSM) met en évidence où le temps et la valeur "
            "se perdent.</p>"
            "<p>Utilisées ensemble, ces méthodes transforment un processus vague et "
            "interconnecté en quelque chose de visible, porté et mesurable - condition "
            "préalable à toute amélioration réelle.</p>"
        ),
        "how": (
            "<h3>How is the method applied?</h3>"
            "<p>The approach follows four practical steps that build on one another.</p>"
            "<p>First, identify the key processes worth mapping - those that are critical, "
            "costly or a frequent source of friction.</p>"
            "<p>Second, build the SIPOC / VSM diagrams: list suppliers, inputs, process steps, "
            "outputs and customers, then visualize the end-to-end flow to surface delays and "
            "rework.</p>"
            "<p>Third, apply the RACI matrix so that each step has one clear accountable owner "
            "and well-defined responsible, consulted and informed parties.</p>"
            "<p>Finally, communicate the maps to the teams and implement the changes the "
            "analysis reveals, then iterate.</p>"
        ),
        "how_fr": (
            "<h3>Comment la méthode est-elle appliquée ?</h3>"
            "<p>La démarche suit quatre étapes concrètes qui s’enchaînent.</p>"
            "<p>D’abord, identifier les processus clés à cartographier - ceux qui sont "
            "critiques, coûteux ou sources fréquentes de frictions.</p>"
            "<p>Ensuite, construire les diagrammes SIPOC / VSM : lister fournisseurs, entrées, "
            "étapes du processus, sorties et clients, puis visualiser le flux de bout en bout "
            "pour faire apparaître délais et reprises.</p>"
            "<p>Puis, appliquer la matrice RACI afin que chaque étape ait un responsable "
            "clairement identifié, ainsi que des acteurs responsables, consultés et informés "
            "bien définis.</p>"
            "<p>Enfin, communiquer les cartographies aux équipes et mettre en œuvre les "
            "changements révélés par l’analyse, puis itérer.</p>"
        ),
        "what": (
            "<h3>Where does it apply?</h3>"
            "<p>The SIPOC / RACI / VSM combination is deliberately generic, so it fits very "
            "different contexts.</p>"
            "<ol>"
            "<li><strong>Software development</strong>: map requirements, build and test "
            "processes, and clarify coding, review and validation responsibilities.</li>"
            "<li><strong>Project management</strong>: chart the planning, execution and "
            "monitoring processes and assign ownership at each stage.</li>"
            "<li><strong>Process improvement</strong>: expose inefficiencies and bottlenecks "
            "in existing workflows and prioritize what to optimize first.</li>"
            "</ol>"
            "<p>In every case the goal is the same: replace assumptions with a shared, explicit "
            "picture of how work really flows.</p>"
        ),
        "what_fr": (
            "<h3>Où s’applique-t-elle ?</h3>"
            "<p>La combinaison SIPOC / RACI / VSM est volontairement générique, ce qui lui "
            "permet de s’adapter à des contextes très différents.</p>"
            "<ol>"
            "<li><strong>Développement logiciel</strong> : cartographier les besoins, les "
            "processus de réalisation et de test, et clarifier les responsabilités de "
            "développement, de revue et de validation.</li>"
            "<li><strong>Gestion de projet</strong> : cartographier les processus de "
            "planification, d’exécution et de suivi et attribuer un responsable à chaque "
            "étape.</li>"
            "<li><strong>Amélioration des processus</strong> : mettre en évidence les "
            "inefficacités et les goulets d’étranglement des flux existants et prioriser ce "
            "qu’il faut optimiser en premier.</li>"
            "</ol>"
            "<p>Dans tous les cas, l’objectif est le même : remplacer les suppositions par une "
            "vision partagée et explicite de la façon dont le travail s’écoule réellement.</p>"
        ),
        "conclusion": (
            "<p>SIPOC, RACI and VSM are not paperwork for its own sake: they are levers to make "
            "complex processes clear, accountable and efficient.</p>"
            "<p>Whether you need to observe, improve or simplify your processes, OAAS can help "
            "you turn a tangled workflow into a shared, optimized one.</p>"
        ),
        "conclusion_fr": (
            "<p>SIPOC, RACI et VSM ne sont pas de la paperasse pour elle-même : ce sont des "
            "leviers pour rendre les processus complexes clairs, responsabilisés et "
            "efficaces.</p>"
            "<p>Que vous ayez besoin d’observer, d’améliorer ou de simplifier vos processus, "
            "OAAS peut vous aider à transformer un flux de travail enchevêtré en un flux "
            "partagé et optimisé.</p>"
        ),
        "summary": (
            "<p>In process management, combining the <strong>SIPOC</strong> method with the "
            "<strong>RACI</strong> matrix and <strong>value-stream mapping (VSM)</strong> "
            "clarifies workflows, defines roles and responsibilities, and improves operational "
            "efficiency. This article explains why the combination matters, how to apply it "
            "step by step, and where it delivers value.</p>"
        ),
        "summary_fr": (
            "<p>En gestion des processus, combiner la méthode <strong>SIPOC</strong> avec la "
            "matrice <strong>RACI</strong> et la <strong>cartographie de la chaîne de valeur "
            "(VSM)</strong> clarifie les flux de travail, définit les rôles et responsabilités "
            "et améliore l’efficacité opérationnelle. Cet article explique pourquoi cette "
            "combinaison compte, comment l’appliquer étape par étape, et où elle apporte de la "
            "valeur.</p>"
        ),
        "adv_label": "Clear, shared processes",
        "adv_label_fr": "Des processus clairs et partagés",
    },
]

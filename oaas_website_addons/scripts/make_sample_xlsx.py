# -*- coding: utf-8 -*-
"""
Genere un fichier .xlsx compatible avec l'import blog.post.import
(feuille "Blog import", 22 colonnes 0-indexees).

Reprend le texte de l'article "IOTPlatform" (cf. capture du builder Odoo).
Le contenu est fourni EN ANGLAIS dans les colonnes EN : le pipeline d'import
traduira automatiquement vers le FR via translate (langue source != cible,
ce qui evite l'erreur "PLEASE SELECT TWO DISTINCT LANGUAGES").

Usage :
    python make_sample_xlsx.py
    -> ecrit OAAS_BLOG_POST_IOTPlatform.xlsx a cote du script
"""
import os
import openpyxl

# --- En-tetes (ligne 0, ignoree a l'import) --------------------------------
HEADERS = [
    "Blog",                    # 0  blog.blog name (lookup)
    "Title",                   # 1  name (EN)
    "Subtitle",                # 2  subtitle (EN)
    "(unused)",                # 3
    "Website",                 # 4  website name (lookup)
    "Author email",            # 5  res.users email (lookup)
    "Post date",               # 6  dd/mm/yyyy HH:MM:SS
    "Meta title",              # 7
    "Meta description",        # 8
    "Meta keywords",           # 9
    "is_published",            # 10 bool str
    "active",                  # 11 bool str
    "Why text",                # 12
    "How text",                # 13
    "What text",               # 14
    "Conclusion text",         # 15
    "Cover image",             # 16 (image anchor)
    "Why image",               # 17 (image anchor)
    "How image",               # 18 (image anchor)
    "What image",              # 19 (image anchor)
    "Conclusion image",        # 20 (image anchor)
    "Summary",                 # 21 resume (intro, EN, rendu en haut de l'article)
    "Advantages (HTML)",       # 22 accordeon optionnel : HTML brut colle du builder
    "to_import",               # 23 bool str
]

# --- Corps de l'article (HTML builder insere tel quel dans le content) ------
# NB : les titres internes sont en <h3> (les titres de section sont des <h2>),
# pour une hierarchie de titres correcte cote SEO.
WHY = (
    "<h3>Why build a programmable IoT platform?</h3>"
    "<p>An <strong>IoT project</strong> often starts simply: read a temperature, track "
    "a level, measure a consumption or trigger a device remotely. At this stage, a "
    "script or a simple dashboard is often enough.</p>"
    "<p>But as soon as the project grows, the needs become more complex: several "
    "devices, several users, several sites, access rights, history, alerts, business "
    "rules, exports and security. Maintaining a custom-built tool quickly becomes "
    "costly and fragile.</p>"
    "<p><strong>IOTPlatform</strong> answers this need by centralizing the management "
    "of connected equipment in a single, adaptable and scalable solution. Instead of "
    "rebuilding everything for each project, you rely on a proven foundation.</p>"
    "<p>The goal is not only to connect objects. The goal is to turn field data into "
    "useful information, and then into concrete actions that create real business "
    "value.</p>"
)

HOW = (
    "<h3>How does the platform work?</h3>"
    "<p>The platform relies on a simple logic: <strong>connect, collect, visualize and "
    "automate</strong>. Each step builds on the previous one to turn raw signals into "
    "decisions.</p>"
    "<p>First, devices are added in the interface. Each piece of equipment can be "
    "configured according to its type, its expected data, its possible actions and its "
    "business rules.</p>"
    "<p>Then, the devices send their data to the platform. This information is stored, "
    "historized and displayed in readable dashboards, so teams always have an accurate "
    "view of the field.</p>"
    "<p>Finally, the user can create scenarios: send an alert, trigger an action, "
    "notify a team or connect the platform to another tool through its API.</p>"
    "<h3>Main features</h3>"
    "<p>The platform makes it possible to manage connected devices, collect field data, "
    "visualize measurements, create automation rules, generate alerts and secure "
    "access with role-based permissions.</p>"
    "<p>It can adapt to different technical contexts, in particular with "
    "<strong>LoRa</strong>, <strong>Sigfox</strong> devices, REST APIs or custom "
    "frames, which makes it suitable for both new deployments and existing fleets.</p>"
)

WHAT = (
    "<h3>What can you build with this platform?</h3>"
    "<p>The platform can be used for many IoT use cases: building supervision, energy "
    "monitoring, connected maintenance, actuator control, alert management, multi-site "
    "monitoring or environmental surveillance.</p>"
    "<p>A few concrete examples:</p>"
    "<ol>"
    "<li>Monitor the temperature and humidity of a building.</li>"
    "<li>Track the energy consumption of a site.</li>"
    "<li>Control equipment remotely.</li>"
    "<li>Trigger alerts in case of anomaly.</li>"
    "<li>Automate an action based on a threshold or a schedule.</li>"
    "<li>Centralize the data of several devices in a single interface.</li>"
    "</ol>"
    "<h3>Create your first use case</h3>"
    "<p>A first scenario can be set up progressively: creating the space, adding "
    "devices, defining the data to track, configuring the business rules, then "
    "reviewing the results in the dashboard.</p>"
    "<p>This approach makes it possible to start simply, then evolve the solution "
    "according to the real needs of the field, without rebuilding everything as your "
    "requirements grow.</p>"
)

CONCLUSION = (
    "<p>With its programmable IoT platform, OAAS offers a foundation able to connect "
    "devices, collect data, automate actions and build interfaces tailored to business "
    "needs.</p>"
    "<p>It allows companies to better monitor their equipment, react faster to "
    "anomalies and turn their field data into levers for action.</p>"
    "<p>Whether you are starting your first connected project or industrializing an "
    "existing fleet, IOTPlatform gives you a reliable base to grow on. "
    "<strong>Let's talk about your IoT project.</strong></p>"
)

SUMMARY = (
    "<p><strong>IOTPlatform</strong> is a programmable IoT platform that centralizes the "
    "management, monitoring and remote control of your connected devices. This article "
    "explains why such a platform matters, how it works, what you can build with it, and "
    "how to start your first use case in minutes rather than months.</p>"
)

# Accordeon "Your benefits" : source anglaise traduite vers le francais
# par le pipeline d'import, comme les autres contenus de l'article.
# Les IDs (myCollapse*) sont rendus uniques par post a l'import.
ADVANTAGES = (
    '<h3>Your benefits</h3>'
    '<div id="myCollapse" class="accordion" role="tablist">'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="true" class="card-header s_faq_collapse_right_icon" data-bs-target="#myCollapseTab1">Lower development costs</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab1" class="collapse show">'
    '<div class="card-body"><p class="card-text">The platform already provides the essential building blocks: device management, data collection, dashboards, alerts, security and automation. You save development time and focus your effort on business needs.</p></div>'
    '</div></div>'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab2">Reusable foundation</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab2" class="collapse">'
    '<div class="card-body"><p class="card-text">Instead of rebuilding a complete solution for every IoT project, OAAS relies on a scalable technical foundation that can adapt to different uses, industries and field constraints.</p></div>'
    '</div></div>'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab3">Centralized fleet management</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab3" class="collapse">'
    '<div class="card-body"><p class="card-text">All sensors, actuators and connected equipment are monitored from a single interface. Teams can review device status, latest data and configuration without multiplying tools.</p></div>'
    '</div></div>'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab4">Actionable data</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab4" class="collapse">'
    '<div class="card-body"><p class="card-text">Field data is collected, historized and transformed into understandable indicators. The goal is not only to store measurements, but to make them useful for decisions and actions.</p></div>'
    '</div></div>'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab5">Business automation</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab5" class="collapse">'
    '<div class="card-body"><p class="card-text">The platform can trigger actions according to rules: threshold exceeded, scheduled time, detected anomaly or specific event. This reduces manual intervention and improves responsiveness.</p></div>'
    '</div></div>'
    '<div class="card bg-white" data-name="Item">'
    '<a href="#" role="tab" data-bs-toggle="collapse" aria-expanded="false" class="card-header s_faq_collapse_right_icon collapsed" data-bs-target="#myCollapseTab6">Stronger security</a>'
    '<div data-bs-parent="#myCollapse" role="tabpanel" id="myCollapseTab6" class="collapse">'
    '<div class="card-body"><p class="card-text">Access can be controlled according to user roles. Each profile receives only the required permissions: viewing, configuration, control or administration.</p></div>'
    '</div></div>'
    '</div>'
)

ROW = [
    "Projects",                                                     # 0  Blog (EN name, lookup)
    "Why build a programmable IoT platform?",                      # 1  Title (EN)
    "The first programmable IoT platform for managing, monitoring "  # 2  Subtitle (EN)
    "and remotely controlling your connected devices",
    "",                                                             # 3
    "OAAS",                                                         # 4  Website (lookup)
    "vfortin@oaas.fr",                                             # 5  Author email (lookup)
    "23/06/2026 09:00:00",                                         # 6  Post date
    "Programmable IoT Platform | Manage & Monitor Devices | OAAS",  # 7 meta title (~57 car)
    "IOTPlatform by OAAS centralizes management, monitoring and "    # 8 meta description (~150 car)
    "remote control of your connected devices. Collect data, automate "
    "actions and scale IoT projects faster.",
    "IoT platform, programmable IoT, device management, remote "    # 9 meta keywords
    "monitoring, IoT automation, connected devices, LoRa, Sigfox, OAAS",
    "True",                                                        # 10 is_published
    "True",                                                        # 11 active
    WHY,                                                           # 12 Why
    HOW,                                                           # 13 How
    WHAT,                                                          # 14 What
    CONCLUSION,                                                    # 15 Conclusion
    "", "", "", "", "",                                            # 16-20 images (vides)
    SUMMARY,                                                       # 21 Summary (intro)
    ADVANTAGES,                                                    # 22 Advantages (HTML accordeon)
    "True",                                                        # 23 to_import
]


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Blog import"
    ws.append(HEADERS)
    ws.append(ROW)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "OAAS_BLOG_POST_IOTPlatform.xlsx")
    wb.save(out)
    print("Ecrit :", out)


if __name__ == "__main__":
    main()

# Audit de l’existant — FluxCity

Date : 16 octobre 2026. Périmètre : copie locale du projet, fichiers suivis et non suivis par Git, configuration, code source et vérifications locales. Révision de référence : `9ce87a4` (`backend config`).

## 1. Synthèse

FluxCity se situe au stade de **socle technique initial**, avant le développement des fonctionnalités métier. Trois applications sont présentes : une interface React, un backend Java Spring Boot et une API Python FastAPI. Leur découpage correspond à l’intention du cahier des charges, mais aucun parcours utilisateur de simulation n’est encore réalisé de bout en bout.

L’interface affiche la page de démonstration Vite. Le backend Java contient une classe de démarrage, une configuration Actuator et un test de chargement du contexte. L’API Python expose uniquement un endpoint de santé. Aucun graphe PMR, calcul d’itinéraire, scénario de travaux, stockage, moteur d’agents ou rendu cartographique n’a été trouvé.

Les points prioritaires sont la reproductibilité des environnements, la sauvegarde du travail Python dans Git, la documentation de démarrage et la définition d’un premier parcours métier testable. La multiplication des services techniques prévus doit suivre les besoins effectivement implémentés.

## 2. Dépôts et organisation

### Dépôt Git constaté

Un seul dépôt Git est présent dans le périmètre inspecté : **`Flux_City`**, dont l’origine configurée est `https://github.com/whitefoxxyt/Flux_City.git`. Il s’agit d’un **monorepo** : les trois applications ne sont pas des dépôts autonomes. Aucun `.git` imbriqué ni fichier `.gitmodules` n’a été trouvé.

Cette observation décrit le workspace local ; elle ne constitue pas un inventaire des autres dépôts éventuels d’une organisation GitHub. Le dépôt distant n’a pas été interrogé.

| Répertoire | Contenu constaté | État |
|---|---|---|
| `apps/frontend` | Application React/TypeScript/Vite | Suivie par Git, interface de démonstration |
| `apps/backend` | Application Spring Boot/Maven | Suivie par Git, socle de démarrage |
| `apps/simulation-api` | Application FastAPI et environnement uv | Présente localement, entièrement non suivie par Git au début de l’audit |
| `packages` | Aucun fichier | Répertoire réservé, sans bibliothèque partagée |
| `services` | Aucun fichier | Répertoire réservé, sans service implémenté |
| `infrastructure` | Aucun fichier | Aucun déploiement décrit |
| `docs` | Vide avant cet audit | Documentation transverse à créer |
| `.github` | Aucun fichier | Aucun workflow CI/CD présent dans cette copie |

Les répertoires vides ne sont pas conservés par Git : leur présence locale ne garantit pas leur création lors d’un clone.

Quatre commits sont visibles dans l’historique local, tous datés du 14 octobre 2026 : initialisation du dépôt, initialisation du frontend, initialisation du backend et configuration du backend. Le cahier des charges PDF est également non suivi par Git. Aucun changement existant n’a été ajouté à l’index pendant l’audit.

### Éléments transverses

- `README.md` racine : vide.
- `compose.yaml` : vide ; aucun service Docker Compose n’est défini.
- `.gitignore` racine : vide ; des exclusions existent pour Java et le frontend, mais aucune exclusion Python locale n’a été trouvée.
- `.editorconfig` : sans règle exploitable.
- Aucun Dockerfile, migration de base de données ou contrat d’intégration entre applications n’a été trouvé.

## 3. Technologies et réalisations par application

Les versions ci-dessous sont celles déclarées dans les fichiers locaux. Elles ne constituent pas une validation de leur maintenance, de leur sécurité ou de leur disponibilité sur les registres publics.

### 3.1. Frontend — `apps/frontend`

**Technologies présentes :** React et React DOM `^19.2.8`, TypeScript `~6.0.2`, Vite `^8.3.0`, plugin React `^6.1.1`, ESLint `^10.10.0`, CSS. Gestion des dépendances npm avec `package-lock.json` suivi par Git. Le build local utilise Vite `8.3.4`.

**Développements constatés :**

- Montage de l’application avec `createRoot` et `StrictMode` dans `src/main.tsx`.
- Composant `App.tsx` avec compteur interactif, logos et liens de documentation React/Vite.
- Feuilles de style et assets de démonstration.
- Scripts de développement, compilation, lint et prévisualisation.
- Contrôles TypeScript sur les variables et paramètres inutilisés ; configuration ESLint pour TypeScript et les hooks React.

**Fonctionnalités absentes :** carte, visualisation 3D, profils PMR, création de scénarios, dashboard, exports, authentification et appels aux backends. Aucun routeur ou dispositif de tests frontend n’est déclaré. Le fichier Vite ne définit pas de proxy API.

**Améliorations :** remplacer la démonstration par un premier parcours métier ; définir les états de chargement et d’erreur ainsi que le contrat API ; activer explicitement `strict` dans TypeScript après vérification du code ; prévoir des interactions utilisables au clavier et une alternative textuelle à la future carte. Les règles actuelles de compilation ne remplacent pas des tests fonctionnels.

**Preuves :** `package.json`, `src/App.tsx`, `src/main.tsx`, `vite.config.ts`, `eslint.config.js`, `tsconfig.app.json`.

### 3.2. Backend applicatif — `apps/backend`

**Technologies présentes :** Spring Boot `4.1.1`, Maven avec wrapper, Spring Web MVC, Actuator, Validation et dépendances de test Spring/JUnit. Le `pom.xml` fixe `java.version` à **17**, tandis que le README annonce **Java 25 LTS**. La machine d’audit utilise Java 25.

**Développements constatés :**

- Classe `BackendApplication` annotée `@SpringBootApplication`.
- Nom d’application `fluxcity-backend`, port HTTP `8080`.
- Configuration d’exposition des endpoints Actuator `health` et `info`, sans détails de santé.
- Test `contextLoads()` destiné à vérifier le démarrage du contexte Spring.
- README expliquant le lancement et l’intention de gérer les projets de travaux, scénarios et alertes.

**Fonctionnalités absentes :** contrôleur métier, service métier, entité, repository, accès à une base, migration, authentification, rôles et client de l’API Python. La présence de la dépendance Validation ne signifie pas qu’un modèle métier est validé : aucun DTO métier n’existe.

**Améliorations :** aligner la version Java du README et du POM ; définir les responsabilités Java/Python ; implémenter une première API de scénario et ses erreurs ; choisir ensuite la persistance nécessaire. Le README renvoie à un `CONTRIBUTING.md` absent. Les métadonnées du POM, notamment nom, description et licence, restent à renseigner.

**Preuves :** `pom.xml`, `README`, `src/main/java/fr/fluxcity/backend/BackendApplication.java`, `src/main/resources/application.properties`, `src/test/java/fr/fluxcity/backend/BackendApplicationTests.java`.

### 3.3. API de simulation — `apps/simulation-api`

**Technologies présentes :** Python, FastAPI `>=0.143.1`, Uvicorn `>=0.54.0`, gestion et packaging uv/`uv_build`. Outils de développement déclarés : pytest, HTTPX et Ruff. Organisation Python sous `src/`.

**Développements constatés :**

- Instance FastAPI dans `src/fluxcity_simulation_api/main.py`.
- Route `GET /health`, renvoyant `{"status": "UP"}`.
- Routes de documentation FastAPI enregistrées : `/docs`, `/redoc`, `/openapi.json`.
- Configuration Ruff et pytest dans `pyproject.toml`.
- Répertoire `tests/` présent mais vide.

**Écarts concrets :**

1. `pyproject.toml` exige Python `>=3.13,<3.14`, mais `.python-version` indique `3.14`, le lockfile exige `>=3.14` et l’environnement local exécute Python `3.14.8`. L’environnement installé n’atteste donc pas le bon fonctionnement de la configuration déclarée.
2. Le script `fluxcity-simulation-api` cible `fluxcity_simulation_api.main:main`, alors que `main.py` ne définit aucune fonction `main`. Une fonction homonyme existe dans `__init__.py`, où elle imprime seulement un message. Le point d’entrée déclaré ne peut pas démarrer le serveur en l’état. La commande Uvicorn utilisant `fluxcity_simulation_api.main:app` constitue une voie de lancement distincte, à documenter et vérifier.
3. Le paquet est versionné `0.1.0`, tandis que l’application FastAPI annonce `1.0.0`.
4. Le README est vide et l’application n’est pas suivie par Git.
5. Aucune exclusion locale ne protège `.venv/`, `__pycache__/` ou `.ruff_cache/` d’un ajout accidentel. Il faut ajouter les exclusions avant de versionner ce module.

**Fonctionnalités absentes :** ingestion OSM, graphe accessible, routage, contraintes PMR, scénarios, simulation d’agents, traitements asynchrones, stockage et communication avec Java.

**Améliorations :** harmoniser la version Python et régénérer le lockfile ; corriger le point d’entrée ; documenter l’installation et le lancement ; versionner le code et le lockfile après nettoyage des exclusions ; ajouter des tests HTTP et des tests de routage quand le moteur sera introduit. La route de santé confirme seulement une réponse du processus, sans contrôler de données ou de dépendances externes.

**Preuves :** `pyproject.toml`, `.python-version`, `uv.lock`, `src/fluxcity_simulation_api/main.py`, `src/fluxcity_simulation_api/__init__.py`.

## 4. Écart avec le cahier des charges

Référence : `G9_OpenInnovation-CDC-B3_V0.pdf`, version 1.0 du 19 mai 2026, notamment pages 11 à 15 et 19 à 21. Les technologies et fonctionnalités annoncées dans ce document sont des objectifs, pas des réalisations constatées.

| Domaine attendu | Constat dans le code local |
|---|---|
| Graphe viaire PMR : OSMnx, NetworkX, enrichissement géospatial | Aucun module, jeu de données ou pipeline trouvé |
| Routage A* et déviations accessibles | Aucun algorithme ou endpoint métier trouvé |
| Création, sauvegarde et comparaison de scénarios | Aucun modèle, API ou écran trouvé |
| Simulation d’agents Mesa/SimPy | Aucun moteur ni dépendance correspondante trouvés |
| Visualisation CesiumJS/Deck.gl | React présent ; aucune dépendance ou vue cartographique trouvée |
| Dashboard, KPI, exports PDF/vidéo | Aucun développement trouvé |
| PostgreSQL/PostGIS et TimescaleDB | Aucune configuration, dépendance de persistance ou migration trouvée |
| Celery et Redis | Aucune tâche, file ou configuration trouvée |
| Authentification JWT et rôles | Aucun mécanisme applicatif trouvé |
| Docker Compose et déploiement | Fichier Compose vide, aucun Dockerfile trouvé |
| Documentation et tests | Socle partiel ; absence de documentation produit et de tests métier |

Les objectifs de simulation en moins de 30 secondes, de rendu à 30 images/seconde, de couverture des données et de validation terrain ne sont pas mesurables avec l’implémentation actuelle. Aucun pourcentage d’avancement fonctionnel fiable ne peut être déduit du seul nombre de dossiers ou de technologies initialisées.

## 5. Vérifications réalisées et limites

| Vérification | Résultat |
|---|---|
| Frontend : `npm run build` | Réussite, compilation TypeScript et génération Vite |
| Frontend : `npm run lint` | Réussite |
| Python : `.venv/bin/ruff check .` | Réussite |
| Python : `.venv/bin/python -m pytest` | Zéro test collecté ; ne constitue pas une validation fonctionnelle |
| Python : appel direct de `health_check()` et inspection des routes | Retour attendu et routes enregistrées confirmés ; aucun transport HTTP vérifié par ce contrôle |
| Python : essai HTTP via `TestClient` | Aucune réponse obtenue pendant l’essai ; vérification HTTP non concluante dans cet environnement |
| Java : `./mvnw -o test` | Exécution empêchée par l’absence en cache de `maven-surefire-plugin:3.5.6` après résolution de la restriction d’accès au cache Maven |
| Java : `./mvnw test` avec accès au cache et au registre Maven | Réussite après récupération des dépendances : un test exécuté, zéro échec ; contexte Spring démarré sous Java 25 |

Le build et le lint frontend ont été exécutés avec les dépendances déjà installées. Ils ne prouvent pas qu’un clone vierge se réinstalle correctement. Les contrôles Python utilisent un environnement dont la version est incompatible avec l’exigence du manifeste. Les endpoints Java décrits par la configuration ne doivent pas être considérés comme validés en HTTP par cet audit.

Le test Java réussit avec les classes déjà compilées présentes dans `target/` ; aucune recompilation propre sous Java 17 n’a été réalisée. Maven indique que les classes sont à jour. Le succès confirme le chargement du contexte dans l’environnement local, sans résoudre l’écart de versions documentaires.

Aucun audit de vulnérabilités des dépendances, test de charge, examen d’une production ou inventaire distant des workflows, issues et protections de branches n’a été réalisé. Aucune faille exploitable n’est déduite de la seule absence de fonctionnalités de sécurité à ce stade.

## 6. Points d’amélioration prioritaires

| Priorité | Action | Motif et résultat attendu |
|---|---|---|
| P0 — reprise | Ajouter les exclusions Python, puis versionner les sources et le lockfile de simulation | Permettre à un autre développeur de récupérer les trois applications sans embarquer l’environnement virtuel |
| P0 — reprise | Aligner Python, son lockfile et son environnement ; aligner Java et sa documentation | Disposer d’une référence explicite et reproductible pour les runtimes |
| P0 — reprise | Corriger le point d’entrée Python et remplir le README racine et celui de l’API | Permettre installation, lancement et contrôle des trois composants depuis un clone vierge |
| P1 — architecture | Documenter les responsabilités Java/Python et les contrats REST | Éviter la duplication des règles métier et définir formats géographiques, erreurs et versions d’API |
| P1 — produit | Réaliser un premier parcours : sélectionner origine/destination et profil, fermer un tronçon, calculer puis afficher la déviation | Prouver la valeur métier avant d’étendre la stack |
| P1 — données | Définir un petit graphe de référence versionné, les profils PMR et la gestion des attributs manquants | Rendre les calculs explicables et éviter de présenter une accessibilité inconnue comme garantie |
| P1 — qualité | Ajouter une CI de build/lint/tests pour les trois applications | Vérifier les installations reproductibles et détecter les régressions à chaque changement |
| P1 — tests | Tester les cas trajet possible, trajet impossible, fermeture, contraintes PMR et erreurs d’API | Valider les règles métier plutôt que le seul démarrage des frameworks |
| P1 — intégration | Fournir un environnement local documenté et un Compose fonctionnel pour les services nécessaires | Rendre le parcours complet exécutable par l’équipe |
| P2 — sécurité | Implémenter validation, autorisations et authentification avant exposition de données métier | Encadrer les droits de lecture/modification et les paramètres des calculs |
| P2 — accessibilité | Définir navigation clavier, restitution textuelle, contrastes et réduction des animations dès les premiers écrans | Intégrer l’accessibilité au produit dès sa conception |
| P2 — exploitation | Ajouter logs structurés, identifiants de simulation et suivi des erreurs/durées | Pouvoir diagnostiquer les calculs et mesurer les objectifs du cahier des charges |
| P2 — gouvernance | Créer `CONTRIBUTING.md`, compléter `.editorconfig`, documenter la licence et les sources de données | Faciliter les contributions et clarifier les conditions de réutilisation |

P0 désigne ici une priorité de reprise du projet, pas une vulnérabilité de sécurité.

Pour l’architecture, conserver une séparation claire : Java gère les projets, scénarios et droits ; Python porte le graphe, les contraintes PMR et les calculs ; React présente les résultats. Il faut formaliser ce choix avec les contrats et les besoins réels de l’équipe. L’adoption de Celery, Redis ou TimescaleDB peut suivre la démonstration d’un besoin de calcul asynchrone, de cache ou de séries temporelles, sans bloquer le premier prototype.

## 7. Ordre de reprise proposé

1. **Stabiliser le socle** : sources suivies, versions cohérentes, point d’entrée corrigé, commandes documentées et CI minimale. Critère de sortie : un clone vierge permet de construire et de lancer chaque application avec les runtimes annoncés.
2. **Valider le noyau PMR** : graphe réduit, profils explicites, routage nominal et après fermeture, tests des impossibilités. Critère de sortie : résultats déterministes et justifiés sur des cas connus.
3. **Relier les applications** : contrat REST, premier écran de scénario et affichage d’un résultat réel. Critère de sortie : démonstration complète reproductible depuis l’interface.
4. **Étendre selon les besoins** : persistance, tâches asynchrones, données réelles, agents, 3D et comparaison de scénarios. Critère de sortie : critères d’acceptation et mesures associés à chaque fonctionnalité.

L’existant fournit ainsi un point de départ technique identifiable, mais ne constitue pas encore un prototype fonctionnel de jumeau numérique PMR.

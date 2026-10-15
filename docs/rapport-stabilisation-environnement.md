# Rapport de stabilisation de l’environnement FluxCity

Date : 16 octobre 2026.

## Résumé

L’environnement de développement a été stabilisé sans ajout de fonctionnalité
métier ni modification de l’architecture. Python cible désormais la version 3.14
de façon cohérente ; Java cible la version 25, conformément à la validation
explicite du projet. Le point d’entrée FastAPI démarre Uvicorn et un test HTTP
vérifie `/health`.

Aucun fichier n’a été supprimé. Aucun ajout à l’index Git, commit ou push n’a été
effectué. Le PDF, l’audit précédent et les autres fichiers locaux préexistants
ont été préservés. Le module conserve son chemin réel `apps/simulation-api`.

## Fichiers modifiés ou créés

| Fichier | Intervention |
|---|---|
| `.gitignore` | Exclusions des environnements, caches, sorties de build, configurations locales et fichiers de secrets courants ; exemples `.env` autorisés |
| `README.md` | Présentation du monorepo, prérequis, installation, démarrage et vérifications des trois applications |
| `apps/backend/pom.xml` | Cible Java passée de 17 à 25 |
| `apps/backend/README` | Alignement explicite sur le POM Java 25, indication de `JAVA_HOME`, correction du renvoi à un guide de contribution absent |
| `apps/frontend/README.md` | Ajout des instructions FluxCity ; référence du modèle initial conservée |
| `apps/simulation-api/pyproject.toml` | Python `>=3.14,<3.15`, cible Ruff `py314` |
| `apps/simulation-api/uv.lock` | Actualisation hors ligne pour la contrainte Python 3.14 |
| `apps/simulation-api/src/fluxcity_simulation_api/main.py` | Fonction `main()` démarrant Uvicorn, lancement par module possible, typage de la réponse de santé et mise en forme |
| `apps/simulation-api/tests/test_health.py` | Nouveau test HTTP du statut 200 et du JSON `{"status": "UP"}` |
| `apps/simulation-api/README.md` | Instructions d’installation, lancement, contrôle HTTP, tests et versionnement |
| `docs/rapport-stabilisation-environnement.md` | Présent rapport |

`.python-version` indiquait déjà `3.14` et n’a pas été modifié.
Le fichier `__init__.py` préexistant a également été conservé tel quel.

## Justification des décisions

- **Python 3.14** : version déjà utilisée par l’environnement local et le lockfile.
  La borne `<3.15` fixe une seule version mineure de référence. Le lockfile exprime
  cette contrainte sous la forme normalisée `==3.14.*`.
- **Java 25** : choix confirmé par l’utilisateur. Le POM cible désormais 25 et la
  documentation existante annonçant Java 25 devient cohérente avec le build.
- **Point d’entrée** : conservation du script déclaré
  `fluxcity-simulation-api = fluxcity_simulation_api.main:main` ; sa fonction cible
  existe désormais et lance le serveur local sur `127.0.0.1:8000`.
- **Test HTTP** : transport ASGI d’HTTPX avec asyncio, pytest et les dépendances
  déjà déclarées. Aucun plugin de test ou nouvelle dépendance n’a été ajouté.
- **Dépendances** : `uv lock --offline` puis `uv sync --locked --offline` ont
  utilisé le cache existant. La synchronisation a reconstruit et réinstallé
  uniquement le paquet local pour vérifier le script installé. FastAPI reste à
  `0.143.1`, Uvicorn à `0.54.0` ; aucune version majeure de framework n’a changé.
- **Préservation** : les fichiers précédemment non suivis sont restés non suivis.
  Les contrôles Git sont uniquement des lectures et des vérifications d’exclusion.

## Contrôles et résultats

Environnement observé : Python 3.14.8, uv 0.13.1, JDK 25.0.4.1,
Node.js 26.11.1 et npm 12.2.0.

| Contrôle | Commande ou méthode | Résultat |
|---|---|---|
| Build frontend | `npm run build` | Réussite, TypeScript et Vite 8.3.4 |
| Lint frontend | `npm run lint` | Réussite |
| Compilation et tests Java | `./mvnw compiler:compile compiler:testCompile test` | Réussite ; compilation du code et des tests avec `release 25` ; un test, zéro échec |
| Cohérence du lockfile | `uv lock --check --offline` | Réussite |
| Synchronisation Python | `uv sync --locked --offline` | Réussite, paquet local réinstallé |
| Lint Python | `.venv/bin/ruff check .` | Réussite |
| Tests Python | `.venv/bin/python -m pytest -v` sous un délai maximal de 20 secondes | Un test HTTP réussi en 0,18 seconde hors sandbox |
| Point d’entrée installé | Exécution de `.venv/bin/fluxcity-simulation-api`, requête réseau locale puis arrêt du processus | Démarrage Uvicorn, réponse HTTP 200 et JSON attendu, arrêt propre |
| Format des modifications | `git diff --check` | Réussite |
| Index Git | `git diff --cached --name-only` | Vide |
| Fichiers Python versionnables | `git ls-files --others --exclude-standard apps/simulation-api` | Sources, tests, README, manifeste, `.python-version` et lockfile visibles |
| Exclusions | `git check-ignore -v` sur environnement, caches, `.env` et clé privée | Exclusions confirmées ; `.env.example` reste autorisé |

Les sept fichiers Python actuellement prêts à être ajoutés manuellement sont :

- `.python-version`
- `README.md`
- `pyproject.toml`
- `uv.lock`
- `src/fluxcity_simulation_api/__init__.py`
- `src/fluxcity_simulation_api/main.py`
- `tests/test_health.py`

### Restrictions de l’environnement et avertissements

L’accès initial d’uv à son cache utilisateur a échoué car ce répertoire est en
lecture seule dans le sandbox. Les opérations uv ont réussi avec l’accès hors
sandbox autorisé. Le cache Maven nécessite également cet accès.

Le test HTTP Python est resté bloqué dans le sandbox et a été interrompu par la
limite de temps. Le même test, sans changement de code, a réussi immédiatement
hors sandbox. Ce résultat indique une limitation de l’environnement restreint ;
aucune erreur de code n’a été mise en évidence par cette exécution. La vérification
réseau du point d’entrée a également été réalisée hors sandbox.

Les tests Java émettent des avertissements Mockito/Byte Buddy concernant le
chargement dynamique d’un agent. Ils n’empêchent pas la réussite actuelle mais
méritent un suivi pour les futurs JDK.

## Limites et problèmes non résolus

- Le module Python n’est toujours pas suivi par Git : ses fichiers sont prêts à
  être ajoutés, mais l’indexation a volontairement été laissée à l’utilisateur.
- Le frontend a été contrôlé avec les dépendances déjà installées ; aucune
  réinstallation npm sur un clone vierge n’a été effectuée.
- La synchronisation Python a été validée depuis le cache de la machine ; une
  installation sur une machine neuve nécessitera l’accès aux registres.
- La version du paquet Python (`0.1.0`) et celle annoncée dans les métadonnées
  OpenAPI (`1.0.0`) restent différentes, comme avant cette intervention. Leur
  convention de versionnement est à définir séparément.
- Le helper de démonstration `main()` dans `__init__.py` est conservé ; le script
  officiel utilise bien la nouvelle fonction dans `main.py`.
- `compose.yaml` reste vide et aucune communication entre applications n’est
  ajoutée. Les README décrivent le démarrage indépendant des applications.
- Les exclusions Git constituent une protection préventive ; elles ne remplacent
  pas une revue des contenus avant indexation, notamment pour des secrets portant
  des noms non conventionnels.

## Prochaine étape recommandée

Relire puis ajouter manuellement les fichiers nécessaires à Git, et valider les
commandes documentées depuis un clone neuf. Mettre ensuite en place une CI
reprenant ces contrôles avec Python 3.14 et Java 25. La définition des contrats
entre services et le premier parcours métier pourront suivre dans une intervention
distincte.

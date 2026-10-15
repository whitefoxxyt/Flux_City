# FluxCity

Plateforme de simulation d’accessibilité urbaine pour les personnes à mobilité
réduite. Le projet contient actuellement les socles des trois applications ; les
fonctionnalités métier ne sont pas encore implémentées.

## Organisation

| Application | Technologies | Guide |
|---|---|---|
| `apps/frontend` | React, TypeScript, Vite | [Frontend](apps/frontend/README.md) |
| `apps/backend` | Java 25, Spring Boot, Maven | [Backend](apps/backend/README) |
| `apps/simulation-api` | Python 3.14, FastAPI, uv | [Simulation](apps/simulation-api/README.md) |

## Prérequis

- Git, JDK 25 et uv ; Python 3.14 installé ou provisionné par uv.
- Node.js compatible avec Vite : `^20.19.0` ou `>=22.12.0`, avec npm.
- Un accès aux registres npm, Maven et PyPI lors de la première installation.

Maven est fourni par le wrapper du backend. Les lockfiles npm et uv doivent être
conservés dans Git. Chaque application se lance dans un terminal distinct.

## Démarrage local

Frontend, depuis `apps/frontend` :

```bash
npm ci
npm run dev
```

Vite affiche l’adresse locale utilisée, généralement `http://localhost:5173`.

Backend, depuis `apps/backend`, avec `JAVA_HOME` pointant vers un JDK 25 :

```bash
./mvnw spring-boot:run
```

Santé : `http://localhost:8080/actuator/health`.

API Python, depuis `apps/simulation-api` :

```bash
uv sync --locked
uv run --locked fluxcity-simulation-api
```

Santé : `http://127.0.0.1:8000/health` ; documentation :
`http://127.0.0.1:8000/docs`.

## Vérifications

Dans le dossier de chaque application :

```bash
# apps/frontend
npm run build
npm run lint

# apps/backend
./mvnw test

# apps/simulation-api
uv lock --check
uv run --locked ruff check .
uv run --locked pytest
```

Les applications ne communiquent pas encore entre elles. `compose.yaml` est
vide : le lancement se fait avec les commandes ci-dessus.

Ne pas ajouter à Git les environnements virtuels, caches ou secrets. Les sources,
tests, configurations et lockfiles doivent pouvoir être versionnés.

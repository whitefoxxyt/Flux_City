# FluxCity — API de simulation

Socle FastAPI : seul `GET /health` est actuellement implémenté. Il renvoie
`200` et `{"status": "UP"}`. Aucun calcul métier n’est encore disponible.

## Prérequis et installation

Utiliser Python **3.14** et uv. `.python-version`, `requires-python`, Ruff et
`uv.lock` ciblent cette version mineure. Depuis `apps/simulation-api` :

```bash
uv sync --locked
```

Cette commande installe le paquet local et les dépendances de développement
déclarées (HTTPX, pytest, Ruff). Elle peut télécharger Python 3.14 s’il manque.
Le backend de build `uv_build` est géré par uv en environnement de build isolé.

## Démarrage

```bash
uv run --locked fluxcity-simulation-api
```

Le point d’entrée lance Uvicorn sur `127.0.0.1:8000`. Pour le rechargement en
développement ou un autre port :

```bash
uv run --locked uvicorn fluxcity_simulation_api.main:app --reload --port 8000
```

Vérification dans un autre terminal :

```bash
curl --fail http://127.0.0.1:8000/health
```

Swagger : `http://127.0.0.1:8000/docs`. Arrêt du serveur : `Ctrl+C`.

## Contrôles

```bash
uv lock --check
uv run --locked ruff check .
uv run --locked pytest
```

Le test de santé effectue une requête HTTP via le transport ASGI d’HTTPX et
contrôle le statut et le JSON. Il utilise asyncio sans plugin pytest additionnel.

Conserver dans Git `pyproject.toml`, `uv.lock`, `.python-version`, les README,
`src/` et `tests/`. Exclure `.venv/`, les caches et les secrets.

import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="FluxCity Simulation API",
    description="API de simulation urbaine pour FluxCity",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Endpoint de vérification de l'état de santé de l'API.
    """
    return {"status": "UP"}


def main() -> None:
    """Démarre le serveur local via le point d’entrée du paquet."""
    uvicorn.run("fluxcity_simulation_api.main:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()


from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.core.database import get_client

app = FastAPI(
    title="ReachRich API",
    description="Smart Personal Financial Management",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "app": "ReachRich",
        "message": "Welcome to ReachRich!",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    try:
        get_client().auth.get_session()
        return {"status": "healthy", "database": "supabase"}
    except Exception as exc:  # pragma: no cover - simple runtime status check
        return {"status": "unhealthy", "database": "supabase", "error": str(exc)}


@app.get("/transactions")
def get_transactions():
    client = get_client()
    response = client.table("transactions").select("*").execute()
    return response.data


from fastapi import FastAPI

from app.core.database import get_client

app = FastAPI(
    title="ReachRich API",
    description="Smart Personal Financial Management",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "app": "ReachRich",
        "message": "Welcome to ReachRich!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    try:
        get_client().auth.get_session()
        return {"status": "healthy", "database": "supabase"}
    except Exception as exc:  # pragma: no cover - simple runtime status check
        return {"status": "unhealthy", "database": "supabase", "error": str(exc)}


@app.get("/todos")
def get_todos():
    client = get_client()
    response = client.table("todos").select("*").execute()
    return response.data

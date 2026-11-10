from fastapi import FastAPI

app = FastAPI(
    title="ReachRich API",
    description="Smart Personal Financial Management",
    version="1.0.0"
)

@app.get("/")

def home():
    return {
    "app": "ReachRich",
        "message": "Welcome to ReachRich!",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

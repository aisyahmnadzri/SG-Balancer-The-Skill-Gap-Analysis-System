from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app = FastAPI(title="SG Balancer")

app.include_router(analyze_router, prefix="/analyze")

@app.get("/")
def health_check():
    return {"status": "running"}

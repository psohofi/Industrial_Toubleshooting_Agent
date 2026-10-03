from fastapi import FastAPI

from app.api.telemetry import router as telemetry_router


app = FastAPI(
    title="Failure Detection API",
    version="0.1.0",
)

app.include_router(telemetry_router)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
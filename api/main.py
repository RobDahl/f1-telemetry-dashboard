from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.f1_service import get_driver_telemetry

app = FastAPI(title="F1 Telemetry API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "f1-telemetry-api"}


@app.get("/telemetry")
async def telemetry(year: int, session: str, driver: str) -> dict:
    return await get_driver_telemetry(year=year, session=session, driver=driver)

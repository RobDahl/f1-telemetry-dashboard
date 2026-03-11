from fastapi import FastAPI, HTTPException
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
    try:
        return await get_driver_telemetry(year=year, session=session, driver=driver)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500, detail=f"Failed to load telemetry: {exc}"
        ) from exc

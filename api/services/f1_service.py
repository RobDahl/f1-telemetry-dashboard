import asyncio
import os

import fastf1
import pandas as pd


def _parse_session_arg(session: str) -> tuple[str, str]:
    session = session.strip()

    for sep in ("|", ":", ","):
        if sep in session:
            event, session_type = (part.strip() for part in session.split(sep, 1))
            if not event or not session_type:
                raise ValueError(
                    "Invalid session format. Use 'Event|SessionType' (e.g. 'Silverstone|R')."
                )
            return event, session_type

    return session, "R"


def _load_telemetry_sync(year: int, session: str, driver: str) -> dict:
    cache_dir = os.path.join(os.path.dirname(__file__), "..", ".fastf1_cache")
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(os.path.abspath(cache_dir))

    event, session_type = _parse_session_arg(session)

    try:
        f1_session = fastf1.get_session(year, event, session_type)
    except Exception as exc:  # noqa: BLE001
        try:
            schedule = fastf1.get_event_schedule(year)
            query = event.casefold()

            resolved_event: str | None = None
            for _, row in schedule.iterrows():
                for field in ("EventName", "OfficialEventName", "Location"):
                    value = row.get(field)
                    if isinstance(value, str) and query in value.casefold():
                        resolved_event = row.get("EventName")
                        break
                if resolved_event:
                    break

            if not resolved_event:
                raise

            f1_session = fastf1.get_session(year, resolved_event, session_type)
            event = resolved_event
        except Exception as schedule_exc:  # noqa: BLE001
            raise ValueError(
                f"Unable to resolve session '{session}' for year {year}. "
                f"FastF1 error: {exc}"
            ) from schedule_exc

    f1_session.load(telemetry=True, laps=True, weather=False, messages=False)

    laps = f1_session.laps.pick_driver(driver)
    if laps is None or laps.empty:
        raise ValueError(f"No laps found for driver '{driver}'")

    fastest_lap = laps.pick_fastest()
    if fastest_lap is None:
        raise ValueError(f"No fastest lap found for driver '{driver}'")

    telemetry = fastest_lap.get_telemetry()
    if telemetry is None or telemetry.empty:
        raise ValueError(f"No telemetry found for driver '{driver}'")

    cols = [c for c in ("Distance", "Speed", "RPM", "nGear") if c in telemetry.columns]
    telemetry = telemetry[cols].copy()
    if "nGear" in telemetry.columns:
        telemetry.rename(columns={"nGear": "Gear"}, inplace=True)

    telemetry = telemetry.where(pd.notnull(telemetry), None)
    records = telemetry.to_dict(orient="records")

    return {
        "year": year,
        "event": event,
        "session_type": session_type,
        "driver": driver,
        "lap_number": int(fastest_lap["LapNumber"]) if "LapNumber" in fastest_lap else None,
        "lap_time": str(fastest_lap["LapTime"]) if "LapTime" in fastest_lap else None,
        "telemetry": records,
    }


async def get_driver_telemetry(year: int, session: str, driver: str) -> dict:
    return await asyncio.to_thread(_load_telemetry_sync, year, session, driver)

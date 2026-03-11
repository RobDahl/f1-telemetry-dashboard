import asyncio
import os
import threading
import time

import fastf1
import numpy as np
import pandas as pd


_SESSION_CACHE_TTL_SECONDS = 60 * 30
_RESPONSE_CACHE_TTL_SECONDS = 60 * 10

_SESSION_CACHE: dict[tuple[int, str, str], tuple[float, object]] = {}
_RESPONSE_CACHE: dict[tuple[int, str, str, str, bool, int | None], tuple[float, dict]] = {}
_CACHE_LOCK = threading.Lock()


def _downsample_df(df: pd.DataFrame, max_points: int) -> pd.DataFrame:
    if max_points <= 0:
        return df

    length = len(df)
    if length <= max_points:
        return df

    idx = np.linspace(0, length - 1, num=max_points, dtype=int)
    idx = np.unique(idx)
    return df.iloc[idx]


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


def _load_telemetry_sync(
    year: int,
    session: str,
    driver: str,
    downsample: bool,
    max_points: int,
) -> dict:
    cache_dir = os.path.join(os.path.dirname(__file__), "..", ".fastf1_cache")
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(os.path.abspath(cache_dir))

    event, session_type = _parse_session_arg(session)

    now = time.monotonic()

    effective_max_points = None if not downsample else max_points
    response_key = (year, event, session_type, driver, downsample, effective_max_points)
    with _CACHE_LOCK:
        cached_response = _RESPONSE_CACHE.get(response_key)
        if cached_response and cached_response[0] > now:
            return cached_response[1]

    resolved_event = event
    try:
        fastf1.get_session(year, resolved_event, session_type)
    except Exception as exc:  # noqa: BLE001
        try:
            schedule = fastf1.get_event_schedule(year)
            query = resolved_event.casefold()

            match: str | None = None
            for _, row in schedule.iterrows():
                for field in ("EventName", "OfficialEventName", "Location"):
                    value = row.get(field)
                    if isinstance(value, str) and query in value.casefold():
                        match = row.get("EventName")
                        break
                if match:
                    break

            if not match:
                raise

            resolved_event = match
        except Exception as schedule_exc:  # noqa: BLE001
            raise ValueError(
                f"Unable to resolve session '{session}' for year {year}. "
                f"FastF1 error: {exc}"
            ) from schedule_exc

    session_key = (year, resolved_event, session_type)
    with _CACHE_LOCK:
        cached_session = _SESSION_CACHE.get(session_key)
        if cached_session and cached_session[0] > now:
            f1_session = cached_session[1]
        else:
            f1_session = None

    if f1_session is None:
        f1_session = fastf1.get_session(year, resolved_event, session_type)
        f1_session.load(telemetry=True, laps=True, weather=False, messages=False)
        with _CACHE_LOCK:
            _SESSION_CACHE[session_key] = (now + _SESSION_CACHE_TTL_SECONDS, f1_session)

    laps = f1_session.laps.pick_drivers([driver])
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

    if downsample:
        telemetry = _downsample_df(telemetry, max_points=max_points)

    records = telemetry.to_dict(orient="records")

    result = {
        "year": year,
        "event": resolved_event,
        "session_type": session_type,
        "driver": driver,
        "lap_number": int(fastest_lap["LapNumber"]) if "LapNumber" in fastest_lap else None,
        "lap_time": str(fastest_lap["LapTime"]) if "LapTime" in fastest_lap else None,
        "telemetry": records,
    }

    with _CACHE_LOCK:
        _RESPONSE_CACHE[(year, resolved_event, session_type, driver, downsample, effective_max_points)] = (
            now + _RESPONSE_CACHE_TTL_SECONDS,
            result,
        )

    return result


async def get_driver_telemetry(
    year: int,
    session: str,
    driver: str,
    downsample: bool = True,
    max_points: int = 2000,
) -> dict:
    return await asyncio.to_thread(
        _load_telemetry_sync,
        year,
        session,
        driver,
        downsample,
        max_points,
    )

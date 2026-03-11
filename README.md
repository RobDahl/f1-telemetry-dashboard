# F1 Telemetry Dashboard

Monorepo for a full stack Formula 1 telemetry dashboard with a Python FastAPI backend (`/api`) and a Next.js frontend (`/web`).

## Stack

- **Backend:** FastAPI, Uvicorn, FastF1, Pandas, NumPy
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Recharts

## Project Structure

```text
f1-telemetry-dashboard/
├─ api/
│  ├─ main.py
│  ├─ requirements.txt
│  └─ services/
│     └─ f1_service.py
├─ web/
│  ├─ app/
│  ├─ components/
│  └─ lib/
└─ package.json
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

## Backend Setup (`/api`)

```bash
python -m venv api/.venv
api/.venv/Scripts/activate
pip install -r api/requirements.txt
python -m uvicorn main:app --reload --port 8000 --app-dir api
```

Backend health endpoint: `http://localhost:8000/`

## Frontend Setup (`/web`)

```bash
npm install --prefix web
npm run dev --prefix web
```

Frontend URL: `http://localhost:3001`

## Run Both Services Together (Recommended)

From the repository root:

```bash
npm install

python -m venv api/.venv
api/.venv/Scripts/activate
pip install -r api/requirements.txt

npm run dev
```

This uses `concurrently` to launch:
- FastAPI at `http://localhost:8000`
- Next.js at `http://localhost:3001`

## Quick Verification

1. Open `http://localhost:8000/` and confirm you receive:
   - `{ "status": "ok", "service": "f1-telemetry-api" }`
2. Open `http://localhost:3001` and confirm the F1 dashboard shell renders.

## Troubleshooting

- If backend dependencies fail to install, ensure pip is up-to-date:
  - `python -m pip install --upgrade pip`
- If port 3001 or 8000 is already in use, stop the conflicting process or change the port in the run command.

# Mock Service API (FastAPI)

This subproject provides mock endpoints for local testing:

- `POST /service-assistant/availability`
- `POST /service-visits/book`
- `POST /service-visits/reschedule`

## Run

```bash
cd mock_service_api
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Health check:

```bash
curl http://127.0.0.1:8001/health
```

## Deploy to Heroku

From repo root (`/Users/rhamsagar/Documents/FastMCP`):

```bash
heroku login
heroku create <your-app-name>
heroku git:remote -a <your-app-name>
git subtree push --prefix mock_service_api heroku main
```

Open health endpoint:

```bash
curl https://<your-app-name>.herokuapp.com/health
```

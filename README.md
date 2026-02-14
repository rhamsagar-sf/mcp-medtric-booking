# mcp-medtric-booking

MCP server for service scheduling, deployable to FastMCP Horizon, with a mock backend API deployable to Heroku.

## FastMCP Tools

- `get_service_assistant_availability`
- `book_service_visit`
- `reschedule_booking`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Set these environment variables (or update `.env`):

- `SERVICE_API_BASE_URL`
- `SERVICE_API_KEY`
- `SERVICE_API_TIMEOUT`
- `SERVICE_API_AVAILABILITY_PATH`
- `SERVICE_API_BOOKING_PATH`
- `SERVICE_API_RESCHEDULE_PATH`

## Run With Local Mock API

Start the mock API subproject first:

```bash
cd mock_service_api
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Then run MCP server in another terminal:

```bash
cd /Users/rhamsagar/Documents/FastMCP
source .venv/bin/activate
fastmcp run my_server.py:mcp
```

## Deploy Mock API To Heroku

Deploy the `mock_service_api` subproject:

```bash
cd /Users/rhamsagar/Documents/FastMCP
heroku login
heroku create <your-app-name>
heroku git:remote -a <your-app-name>
git subtree push --prefix mock_service_api heroku main
```

Then point MCP to Heroku:

```bash
export SERVICE_API_BASE_URL=https://<your-app-name>.herokuapp.com
```

Current deployed mock endpoint:

```bash
export SERVICE_API_BASE_URL=https://immense-oasis-54700-ed56d04c5f65.herokuapp.com
```

## Deploy To FastMCP Horizon

1. Push this repository to GitHub.
2. In Horizon, choose **Deploy MCP Server** and connect this repo.
3. Set the entrypoint to `my_server.py:mcp`.
4. Add required environment variables in Horizon (`SERVICE_API_BASE_URL`, `SERVICE_API_KEY`, etc).
5. Deploy and test tools from the Horizon test panel.

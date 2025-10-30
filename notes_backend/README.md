# Personal Notes Manager - Backend (FastAPI)

FastAPI backend service for a personal notes application. Provides CRUD endpoints for notes persisted in a local SQLite database by default.

## Features

- FastAPI app with auto-generated docs at `/docs` and `/redoc`
- Health endpoint: `GET /healthz` returning `{"status": "ok"}`
- Notes CRUD:
  - POST `/notes`
  - GET `/notes`
  - GET `/notes/{id}`
  - PUT `/notes/{id}`
  - DELETE `/notes/{id}`
- SQLite persistence via SQLAlchemy (`notes.db` by default)
- Runs on port `3001` by default

## Getting Started

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Run the server (port 3001)

Using python entrypoint:

```bash
python -m api
```

Or with uvicorn directly:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 3001
```

Visit the docs at: http://localhost:3001/docs

### Configuration

The service supports the following optional environment variables:

- `PORT`: Port to run the service on (default `3001`)
- `NOTES_DB_URL`: SQLAlchemy database URL (default `sqlite:///./notes.db`)
- `UVICORN_RELOAD`: Set to `true` to enable auto-reload (development)

Provide these in an `.env` file or your environment.

See `.env.example` for a template.

### Project Structure

```
notes_backend/
  src/
    api/
      __init__.py
      __main__.py
      main.py
      db.py
      models.py
      schemas.py
      routers/
        health.py
        notes.py
  requirements.txt
```

### Example Requests

Create a note:
```bash
curl -X POST http://localhost:3001/notes -H "Content-Type: application/json" -d '{"title":"First","content":"Hello"}'
```

List notes:
```bash
curl http://localhost:3001/notes
```

Get note:
```bash
curl http://localhost:3001/notes/1
```

Update note:
```bash
curl -X PUT http://localhost:3001/notes/1 -H "Content-Type: application/json" -d '{"content":"Updated"}'
```

Delete note:
```bash
curl -X DELETE http://localhost:3001/notes/1
```

## Development Notes

- For production, restrict CORS origins in `api/main.py`.
- If you change models, the app auto-creates tables; migrations are not configured.

## License

MIT

# personal-notes-manager-36730-36749

This workspace contains the backend service for a personal notes manager.

- Backend (FastAPI): `notes_backend/`

Quick start:
1. Change directory to the backend:
   ```
   cd notes_backend
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the service on port 3001:
   ```
   python -m src.api
   ```
   or
   ```
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001
   ```

Docs: http://localhost:3001/docs  
Health: http://localhost:3001/healthz

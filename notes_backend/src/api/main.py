from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import notes
from api.routers.health import router as health_router

# Create FastAPI app with metadata for OpenAPI/Swagger
app = FastAPI(
    title="Personal Notes Manager API",
    description="FastAPI backend for managing personal notes with CRUD operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness probes"},
        {"name": "Notes", "description": "CRUD operations for notes"},
    ],
)

# CORS configuration (wide-open for development; restrict in production via env)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(notes.router, prefix="/notes", tags=["Notes"])


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check (root)",
    description="Basic health check endpoint at root path. Prefer /healthz.",
)
def health_check_root():
    """Root health check that returns a simple message."""
    return {"message": "Healthy"}


# Public interface note: The app is intended to be run by Uvicorn on port 3001.
# See README for instructions.

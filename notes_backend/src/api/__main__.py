import os

import uvicorn


def main():
    """
    Launch the FastAPI app using Uvicorn.
    The server listens on port 3001 by default; override with PORT env var.
    """
    port = int(os.getenv("PORT", "3001"))
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("UVICORN_RELOAD", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()

from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "/healthz",
    tags=["Health"],
    summary="Health Check",
    description="Returns service health status. Useful for readiness/liveness probes.",
    responses={200: {"description": "Service is healthy"}},
)
def healthz():
    """Health endpoint returning a simple JSON status."""
    return {"status": "ok"}

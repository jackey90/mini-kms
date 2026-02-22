from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict:
    return {"status": "ok", "version": "1.0.0"}

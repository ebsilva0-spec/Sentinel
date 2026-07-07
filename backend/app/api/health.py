from fastapi import APIRouter

router = APIRouter(
    tags=["Health"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "api": "Sentinel",
        "version": "1.0.0"
    }
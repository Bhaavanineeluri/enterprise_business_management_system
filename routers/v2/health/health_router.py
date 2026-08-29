from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health V2"],
)


@router.get("")
def health_check():
    return {
        "success": True,
        "api_version": "v2",
        "service": "Enterprise Business Management System",
        "status": "operational",
    }

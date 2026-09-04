from fastapi import APIRouter, HTTPException, Query

from services.external_api.external_api_service import call_external_api


router = APIRouter(
    prefix="/external-api",
    tags=["External API"],
)


@router.get("/call")
def call_external_api_endpoint(
    url: str = Query(..., description="External API URL"),
):
    result = call_external_api(url)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )

    return result

from fastapi import APIRouter, Query

from services.concurrent_operations.concurrent_service import (
    run_concurrent_operations,
)


router = APIRouter(
    prefix="/concurrent",
    tags=["Concurrent Operations"],
)


@router.post("/operations")
async def execute_concurrent_operations(
    operations: list[str] = Query(..., min_length=1),
):
    return await run_concurrent_operations(operations)

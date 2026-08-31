from fastapi import (
    APIRouter,
    Depends,
    File as FastAPIFile,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.users.user import User
from schemas.imports.csv_import import CSVImportResponse
from services.imports.csv_import_service import (
    import_employees_from_csv,
)


router = APIRouter(
    prefix="/imports",
    tags=["CSV Import"],
)


@router.post(
    "/employees",
    response_model=CSVImportResponse,
    status_code=status.HTTP_200_OK,
)
async def import_employees_api(
    csv_file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not csv_file.filename:
        raise ValueError(
            "CSV file name is required"
        )

    if not csv_file.filename.lower().endswith(".csv"):
        raise ValueError(
            "Only CSV files are allowed"
        )

    content = await csv_file.read()

    result = import_employees_from_csv(
        db=db,
        csv_content=content,
    )

    return {
        "success": True,
        "message": "CSV import completed",
        **result,
    }

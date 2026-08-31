from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import Response
from sqlalchemy.orm import Session

from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.users.user import User
from services.exports.csv_export_service import (
    export_employees_to_csv,
)


router = APIRouter(
    prefix="/exports",
    tags=["CSV Export"],
)


@router.get(
    "/employees",
)
def export_employees_api(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    csv_content = export_employees_to_csv(
        db
    )

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                'attachment; filename="employees.csv"'
            )
        },
    )

from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    File as FastAPIFile,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from exceptions import ResourceNotFoundException
from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.users.user import User
from schemas.files.file import FileMessageResponse
from services.files.file_service import (
    create_file_record,
    save_uploaded_file,
    get_file,
)


router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@router.put(
    "/{file_id}",
    response_model=FileMessageResponse,
    status_code=status.HTTP_200_OK,
)
def update_file_api(
    file_id: int,
    upload_file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_record = update_file(
        db=db,
        file_id=file_id,
        upload_file=upload_file,
    )

    return {
        "success": True,
        "message": "File updated successfully",
        "data": file_record,
    }


@router.post(
    "/upload",
    response_model=FileMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_file_api(
    upload_file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    (
        original_filename,
        file_path,
        file_size,
    ) = save_uploaded_file(
        upload_file
    )

    file_record = create_file_record(
        db=db,
        original_filename=original_filename,
        file_path=file_path,
        file_size=file_size,
        content_type=upload_file.content_type,
        uploaded_by=current_user.id,
    )

    return {
        "success": True,
        "message": "File uploaded successfully",
        "data": file_record,
    }


@router.get(
    "/download/{file_id}",
)
def download_file_api(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_record = get_file(
        db=db,
        file_id=file_id,
    )

    file_path = Path(file_record.file_path)

    if not file_path.exists():
        raise ResourceNotFoundException(
            "Stored file not found"
        )

    return FileResponse(
        path=file_path,
        media_type=file_record.content_type,
        filename=file_record.original_filename,
    )


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_200_OK,
)
def delete_file_api(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_record = get_file(
        db=db,
        file_id=file_id,
    )

    if file_record.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own files",
        )

    delete_file(
        db=db,
        file_id=file_id,
    )

    return {
        "success": True,
        "message": "File deleted successfully",
    }

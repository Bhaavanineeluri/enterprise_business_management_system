from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from exceptions import ResourceNotFoundException
from models.files.file import File


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
    "text/csv",
}


def create_stored_filename(
    original_filename: str,
) -> str:

    suffix = Path(original_filename).suffix

    return f"{uuid4().hex}{suffix}"


def validate_file(
    upload_file: UploadFile,
) -> None:

    if not upload_file.filename:
        raise ValueError(
            "File name is required"
        )

    if upload_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "Unsupported file type"
        )


def save_uploaded_file(
    upload_file: UploadFile,
) -> tuple[str, str, int]:

    validate_file(upload_file)

    original_filename = upload_file.filename

    stored_filename = create_stored_filename(
        original_filename
    )

    file_path = UPLOAD_DIR / stored_filename

    file_size = 0

    try:
        with file_path.open("wb") as buffer:

            while True:
                chunk = upload_file.file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise ValueError(
                        "File size exceeds the 5 MB limit"
                    )

                buffer.write(chunk)

    except Exception:
        file_path.unlink(
            missing_ok=True
        )
        raise

    return (
        original_filename,
        str(file_path),
        file_size,
    )


def create_file_record(
    db: Session,
    original_filename: str,
    file_path: str,
    file_size: int,
    content_type: str | None,
    uploaded_by: int,
) -> File:

    stored_filename = Path(file_path).name

    file_record = File(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        content_type=content_type,
        file_size=file_size,
        uploaded_by=uploaded_by,
    )

    try:
        db.add(file_record)
        db.commit()
        db.refresh(file_record)

    except Exception:
        db.rollback()

        Path(file_path).unlink(
            missing_ok=True
        )

        raise

    return file_record


def update_file(
    db: Session,
    file_id: int,
    upload_file: UploadFile,
) -> File:

    file_record = get_file(
        db,
        file_id,
    )

    validate_file(upload_file)

    if not upload_file.filename:
        raise ValueError("File name is required")

    original_filename = upload_file.filename
    stored_filename = create_stored_filename(
        original_filename
    )

    new_file_path = UPLOAD_DIR / stored_filename
    file_size = 0

    try:
        with new_file_path.open("wb") as buffer:

            while True:
                chunk = upload_file.file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise ValueError(
                        "File size exceeds the 5 MB limit"
                    )

                buffer.write(chunk)

        old_file_path = Path(file_record.file_path)

        file_record.original_filename = original_filename
        file_record.stored_filename = stored_filename
        file_record.file_path = str(new_file_path)
        file_record.content_type = upload_file.content_type
        file_record.file_size = file_size

        db.commit()
        db.refresh(file_record)

        old_file_path.unlink(missing_ok=True)

    except Exception:
        db.rollback()
        new_file_path.unlink(missing_ok=True)
        raise

    return file_record


def get_file(
    db: Session,
    file_id: int,
) -> File:

    file_record = (
        db.query(File)
        .filter(File.id == file_id)
        .first()
    )

    if file_record is None:
        raise ResourceNotFoundException(
            "File not found"
        )

    return file_record


def delete_file(
    db: Session,
    file_id: int,
) -> None:

    file_record = get_file(
        db,
        file_id,
    )

    Path(file_record.file_path).unlink(
        missing_ok=True
    )

    db.delete(file_record)
    db.commit()

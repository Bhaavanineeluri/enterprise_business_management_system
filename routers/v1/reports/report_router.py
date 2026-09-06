from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.reports.report import (
    ReportCreate,
    ReportListResponse,
    ReportPatch,
    ReportSingleResponse,
    ReportUpdate,
)
from services.reports.report_service import (
    create_report,
    delete_report,
    get_report,
    get_reports,
    restore_report,
    update_report,
)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post(
    "",
    response_model=ReportSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report_api(
    report_data: ReportCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    report = create_report(db, report_data)
    response.headers["Location"] = f"/api/v1/reports/{report.id}"

    return {
        "success": True,
        "message": "Report created successfully",
        "data": report,
    }


@router.get("", response_model=ReportListResponse)
def get_reports_api(
    report_type: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    report_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    reports, total = get_reports(
        db,
        report_type=report_type,
        status=status_filter,
        report_code=report_code,
        offset=offset,
        limit=page_size,
    )

    pages = ((total + page_size - 1) // page_size) if total else 0

    return {
        "success": True,
        "message": "Reports retrieved successfully",
        "data": {
            "items": reports,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get("/{report_id}", response_model=ReportSingleResponse)
def get_report_api(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = get_report(db, report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return {
        "success": True,
        "message": "Report retrieved successfully",
        "data": report,
    }


@router.put("/{report_id}", response_model=ReportSingleResponse)
def update_report_api(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
):
    report = update_report(db, report_id, report_data)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return {
        "success": True,
        "message": "Report updated successfully",
        "data": report,
    }


@router.patch("/{report_id}", response_model=ReportSingleResponse)
def patch_report_api(
    report_id: int,
    report_data: ReportPatch,
    db: Session = Depends(get_db),
):
    report = update_report(db, report_id, report_data)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return {
        "success": True,
        "message": "Report partially updated successfully",
        "data": report,
    }


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report_api(
    report_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_report(db, report_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{report_id}/restore", response_model=ReportSingleResponse)
def restore_report_api(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = restore_report(db, report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted report not found",
        )

    return {
        "success": True,
        "message": "Report restored successfully",
        "data": report,
    }

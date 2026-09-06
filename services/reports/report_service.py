from datetime import datetime

from sqlalchemy.orm import Session

from models.reports.report import Report
from schemas.reports.report import ReportCreate, ReportUpdate


def create_report(db: Session, report_data: ReportCreate) -> Report:
    report = Report(
        report_code=report_data.report_code,
        name=report_data.name,
        report_type=report_data.report_type,
        description=report_data.description,
        status=report_data.status,
        generated_file=report_data.generated_file,
        generated_at=report_data.generated_at,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_report(db: Session, report_id: int) -> Report | None:
    return (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.deleted_at.is_(None),
        )
        .first()
    )


def get_reports(
    db: Session,
    report_type: str | None = None,
    status: str | None = None,
    report_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Report).filter(Report.deleted_at.is_(None))

    if report_type:
        query = query.filter(
            Report.report_type.ilike(f"%{report_type}%")
        )

    if status:
        query = query.filter(
            Report.status.ilike(f"%{status}%")
        )

    if report_code:
        query = query.filter(
            Report.report_code.ilike(f"%{report_code}%")
        )

    total = query.count()

    reports = (
        query.order_by(Report.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return reports, total


def update_report(
    db: Session,
    report_id: int,
    report_data: ReportUpdate,
) -> Report | None:
    report = get_report(db, report_id)

    if report is None:
        return None

    update_data = report_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)

    return report


def delete_report(db: Session, report_id: int) -> bool:
    report = get_report(db, report_id)

    if report is None:
        return False

    report.deleted_at = datetime.now()

    db.commit()

    return True


def restore_report(
    db: Session,
    report_id: int,
) -> Report | None:
    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.deleted_at.is_not(None),
        )
        .first()
    )

    if report is None:
        return None

    report.deleted_at = None

    db.commit()
    db.refresh(report)

    return report

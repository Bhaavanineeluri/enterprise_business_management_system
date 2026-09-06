from datetime import datetime

from sqlalchemy.orm import Session

from models.tasks.task import Task
from schemas.tasks.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
) -> Task:
    task = Task(
        task_code=task_data.task_code,
        title=task_data.title,
        description=task_data.description,
        assigned_to=task_data.assigned_to,
        priority=task_data.priority,
        status=task_data.status,
        due_date=task_data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_task(
    db: Session,
    task_id: int,
) -> Task | None:
    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )


def get_tasks(
    db: Session,
    assigned_to: int | None = None,
    priority: str | None = None,
    status: str | None = None,
    task_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Task).filter(
        Task.deleted_at.is_(None)
    )

    if assigned_to:
        query = query.filter(
            Task.assigned_to == assigned_to
        )

    if priority:
        query = query.filter(
            Task.priority.ilike(f"%{priority}%")
        )

    if status:
        query = query.filter(
            Task.status.ilike(f"%{status}%")
        )

    if task_code:
        query = query.filter(
            Task.task_code.ilike(f"%{task_code}%")
        )

    total = query.count()

    tasks = (
        query.order_by(Task.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return tasks, total


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
) -> Task | None:
    task = get_task(db, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task_id: int,
) -> bool:
    task = get_task(db, task_id)

    if task is None:
        return False

    task.deleted_at = datetime.now()

    db.commit()

    return True


def restore_task(
    db: Session,
    task_id: int,
) -> Task | None:
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.deleted_at.is_not(None),
        )
        .first()
    )

    if task is None:
        return None

    task.deleted_at = None

    db.commit()
    db.refresh(task)

    return task

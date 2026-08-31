from fastapi import APIRouter, BackgroundTasks, status

from schemas.background_tasks.background_task import (
    BackgroundEmailRequest,
    BackgroundNotificationRequest,
    BackgroundTaskResponse,
)
from tasks.email_tasks import send_email_background
from tasks.notification_tasks import (
    create_notification_background,
)


router = APIRouter(
    prefix="/background-tasks",
    tags=["Background Tasks"],
)


@router.post(
    "/email",
    response_model=BackgroundTaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def send_email_api(
    request: BackgroundEmailRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        send_email_background,
        request.recipient,
        request.subject,
        request.message,
    )

    return {
        "success": True,
        "message": "Email scheduled for background processing",
    }


@router.post(
    "/notification",
    response_model=BackgroundTaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_notification_api(
    request: BackgroundNotificationRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        create_notification_background,
        request.user_id,
        request.message,
    )

    return {
        "success": True,
        "message": "Notification scheduled for background processing",
    }

from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

NOTIFICATION_LOG_FILE = (
    LOG_DIR / "notifications.log"
)


def create_notification_background(
    user_id: int,
    message: str,
) -> None:

    timestamp = datetime.now().isoformat()

    log_entry = (
        f"{timestamp} | "
        f"USER_ID={user_id} | "
        f"MESSAGE={message}\n"
    )

    with NOTIFICATION_LOG_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(log_entry)

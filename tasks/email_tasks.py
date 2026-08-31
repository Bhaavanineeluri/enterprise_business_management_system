from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

EMAIL_LOG_FILE = LOG_DIR / "emails.log"


def send_email_background(
    recipient: str,
    subject: str,
    message: str,
) -> None:

    timestamp = datetime.now().isoformat()

    log_entry = (
        f"{timestamp} | "
        f"TO={recipient} | "
        f"SUBJECT={subject} | "
        f"MESSAGE={message}\n"
    )

    with EMAIL_LOG_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(log_entry)

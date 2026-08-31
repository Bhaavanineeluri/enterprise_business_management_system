from apscheduler.schedulers.background import BackgroundScheduler

from scheduler.jobs import cleanup_password_reset_tokens


scheduler = BackgroundScheduler()


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(
        cleanup_password_reset_tokens,
        trigger="interval",
        hours=1,
        id="cleanup_password_reset_tokens",
        replace_existing=True,
    )

    scheduler.start()

    print("[SCHEDULER] Scheduler started")


def stop_scheduler() -> None:
    if not scheduler.running:
        return

    scheduler.shutdown()

    print("[SCHEDULER] Scheduler stopped")

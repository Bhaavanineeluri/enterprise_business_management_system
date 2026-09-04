from unittest.mock import patch

from services.async_processing.async_service import process_async_task


def test_process_async_task():
    with patch(
        "services.async_processing.async_service.time.sleep"
    ) as mock_sleep:

        result = process_async_task("test_task")

    assert result["task_name"] == "test_task"
    assert result["status"] == "completed"

    mock_sleep.assert_called_once_with(5)

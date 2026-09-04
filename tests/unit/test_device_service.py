from unittest.mock import MagicMock, patch

from services.devices.device_service import revoke_device


def test_revoke_device_uses_bulk_update():
    db = MagicMock()

    device = MagicMock()
    device.is_active = True

    device_query = MagicMock()
    device_query.filter.return_value.first.return_value = device

    session_query = MagicMock()
    session_query.filter.return_value.update.return_value = 3

    def query_side_effect(model):
        from models.devices.device import Device
        from models.sessions.session import UserSession

        if model is Device:
            return device_query

        if model is UserSession:
            return session_query

        return MagicMock()

    db.query.side_effect = query_side_effect

    result = revoke_device(
        db=db,
        user_id=1,
        device_id="device-123",
    )

    assert result is True
    assert device.is_active is False

    session_query.filter.return_value.update.assert_called_once()

    update_call = session_query.filter.return_value.update.call_args
    assert update_call.kwargs["synchronize_session"] is False

    db.commit.assert_called_once()

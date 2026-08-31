import re


def validate_password_policy(password: str) -> str:
    if len(password) < 8:
        raise ValueError(
            "password must contain at least 8 characters"
        )

    if len(password) > 128:
        raise ValueError(
            "password must not exceed 128 characters"
        )

    if not any(char.isupper() for char in password):
        raise ValueError(
            "password must contain at least one uppercase letter"
        )

    if not any(char.islower() for char in password):
        raise ValueError(
            "password must contain at least one lowercase letter"
        )

    if not any(char.isdigit() for char in password):
        raise ValueError(
            "password must contain at least one digit"
        )

    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError(
            "password must contain at least one special character"
        )

    return password

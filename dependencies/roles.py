from fastapi import Depends

from dependencies.auth import get_current_user
from exceptions import PermissionDeniedException
from models.users.roles import UserRole
from models.users.user import User


def require_role(*allowed_roles: UserRole):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in [role.value for role in allowed_roles]:
            raise PermissionDeniedException(
                "You do not have permission to access this resource"
            )

        return current_user

    return role_checker

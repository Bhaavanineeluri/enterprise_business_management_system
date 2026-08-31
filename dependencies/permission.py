from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies.auth import get_current_user
from dependencies.database import get_db

from exceptions import PermissionDeniedException

from models.permissions.permission import Permission
from models.role_permissions.role_permission import RolePermission


def require_permission(permission_name: str):

    def permission_checker(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        role = getattr(current_user, "role", None)

        if role is None:
            raise PermissionDeniedException(
                "User role is not assigned"
            )

        permission = (
            db.query(Permission)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .filter(
                RolePermission.role == role,
                Permission.name == permission_name,
            )
            .first()
        )

        if permission is None:
            raise PermissionDeniedException(
                "You do not have permission to access this resource"
            )

        return current_user

    return permission_checker

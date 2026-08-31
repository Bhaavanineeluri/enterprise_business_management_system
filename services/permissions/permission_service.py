from sqlalchemy.orm import Session

from models.permissions.permission import Permission
from models.role_permissions.role_permission import RolePermission


def create_permission(
    db: Session,
    name: str,
    description: str | None = None,
) -> Permission:

    permission = Permission(
        name=name,
        description=description,
    )

    db.add(permission)
    db.flush()

    return permission


def assign_permission_to_role(
    db: Session,
    role: str,
    permission_id: int,
) -> RolePermission:

    role_permission = RolePermission(
        role=role,
        permission_id=permission_id,
    )

    db.add(role_permission)
    db.flush()

    return role_permission

from database import SessionLocal
from models.permissions.permission import Permission
from models.role_permissions.role_permission import RolePermission


PERMISSIONS = [
    ("CREATE_USER", "Create users"),
    ("UPDATE_USER", "Update users"),
    ("DELETE_USER", "Delete users"),
    ("VIEW_USER", "View users"),
]


ROLE_PERMISSIONS = {
    "ADMIN": [
        "CREATE_USER",
        "UPDATE_USER",
        "DELETE_USER",
        "VIEW_USER",
    ],
    "MANAGER": [
        "CREATE_USER",
        "UPDATE_USER",
        "VIEW_USER",
    ],
    "USER": [
        "VIEW_USER",
    ],
}


def seed_permissions():
    db = SessionLocal()

    try:
        permission_map = {}

        for name, description in PERMISSIONS:
            permission = (
                db.query(Permission)
                .filter(Permission.name == name)
                .first()
            )

            if permission is None:
                permission = Permission(
                    name=name,
                    description=description,
                )
                db.add(permission)
                db.flush()

            permission_map[name] = permission

        for role, permission_names in ROLE_PERMISSIONS.items():
            for permission_name in permission_names:
                permission = permission_map[permission_name]

                existing = (
                    db.query(RolePermission)
                    .filter(
                        RolePermission.role == role,
                        RolePermission.permission_id == permission.id,
                    )
                    .first()
                )

                if existing is None:
                    db.add(
                        RolePermission(
                            role=role,
                            permission_id=permission.id,
                        )
                    )

        db.commit()

        print("PERMISSIONS SEEDED SUCCESSFULLY")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_permissions()

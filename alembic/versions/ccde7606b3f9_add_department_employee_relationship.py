"""add department employee relationship

Revision ID: ccde7606b3f9
Revises: 98b993de754d
Create Date: 2026-08-30 12:00:17.347314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ccde7606b3f9'
down_revision: Union[str, Sequence[str], None] = '98b993de754d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create departments table
    op.create_table(
        "departments",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_departments_name"),
        "departments",
        ["name"],
        unique=True,
    )

    # 2. Add department_id temporarily as nullable
    op.add_column(
        "employees",
        sa.Column(
            "department_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_employees_department_id"),
        "employees",
        ["department_id"],
        unique=False,
    )

    # 3. Create departments from existing employee department values
    op.execute(
        """
        INSERT INTO departments (name)
        SELECT DISTINCT department
        FROM employees
        WHERE department IS NOT NULL
        """
    )

    # 4. Connect existing employees to their departments
    op.execute(
        """
        UPDATE employees e
        JOIN departments d
            ON e.department = d.name
        SET e.department_id = d.id
        """
    )

    # 5. Now department_id can safely become NOT NULL
    op.alter_column(
        "employees",
        "department_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # 6. Add the foreign key
    op.create_foreign_key(
        "fk_employees_department_id",
        "employees",
        "departments",
        ["department_id"],
        ["id"],
    )

    # 7. Remove the old string department column
    op.drop_column(
        "employees",
        "department",
    )


def downgrade() -> None:
    # Restore the old department column
    op.add_column(
        "employees",
        sa.Column(
            "department",
            sa.String(length=100),
            nullable=True,
        ),
    )

    # Restore department names
    op.execute(
        """
        UPDATE employees e
        JOIN departments d
            ON e.department_id = d.id
        SET e.department = d.name
        """
    )

    op.alter_column(
        "employees",
        "department",
        existing_type=sa.String(length=100),
        nullable=False,
    )

    op.drop_constraint(
        "fk_employees_department_id",
        "employees",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_employees_department_id"),
        table_name="employees",
    )

    op.drop_column(
        "employees",
        "department_id",
    )

    op.drop_index(
        op.f("ix_departments_name"),
        table_name="departments",
    )

    op.drop_table("departments")
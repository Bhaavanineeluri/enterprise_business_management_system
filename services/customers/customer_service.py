from datetime import datetime

from sqlalchemy.orm import Session

from models.customers.customer import Customer
from schemas.customers.customer import CustomerCreate, CustomerUpdate


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:
    customer = Customer(
        customer_code=customer_data.customer_code,
        company_name=customer_data.company_name,
        contact_name=customer_data.contact_name,
        email=customer_data.email,
        phone=customer_data.phone,
        address=customer_data.address,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customer(
    db: Session,
    customer_id: int,
) -> Customer | None:
    return (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None),
        )
        .first()
    )


def get_customers(
    db: Session,
    name: str | None = None,
    email: str | None = None,
    customer_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Customer).filter(
        Customer.deleted_at.is_(None)
    )

    if name:
        query = query.filter(
            Customer.company_name.ilike(f"%{name}%")
        )

    if email:
        query = query.filter(
            Customer.email.ilike(f"%{email}%")
        )

    if customer_code:
        query = query.filter(
            Customer.customer_code.ilike(
                f"%{customer_code}%"
            )
        )

    total = query.count()

    customers = (
        query.order_by(Customer.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return customers, total


def update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdate,
) -> Customer | None:
    customer = get_customer(db, customer_id)

    if customer is None:
        return None

    update_data = customer_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(
    db: Session,
    customer_id: int,
) -> bool:
    customer = get_customer(db, customer_id)

    if customer is None:
        return False

    customer.deleted_at = datetime.now()

    db.commit()

    return True


def restore_customer(
    db: Session,
    customer_id: int,
) -> Customer | None:
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.deleted_at.is_not(None),
        )
        .first()
    )

    if customer is None:
        return None

    customer.deleted_at = None

    db.commit()
    db.refresh(customer)

    return customer

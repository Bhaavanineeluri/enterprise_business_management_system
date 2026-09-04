from datetime import datetime

from sqlalchemy.orm import Session

from models.orders.order import Order
from schemas.orders.order import OrderCreate, OrderUpdate


def create_order(
    db: Session,
    order_data: OrderCreate,
) -> Order:
    order = Order(
        order_code=order_data.order_code,
        customer_id=order_data.customer_id,
        status=order_data.status,
        total_amount=order_data.total_amount,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_order(
    db: Session,
    order_id: int,
) -> Order | None:
    return (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.deleted_at.is_(None),
        )
        .first()
    )


def get_orders(
    db: Session,
    customer_id: int | None = None,
    status: str | None = None,
    order_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Order).filter(
        Order.deleted_at.is_(None)
    )

    if customer_id:
        query = query.filter(
            Order.customer_id == customer_id
        )

    if status:
        query = query.filter(
            Order.status.ilike(f"%{status}%")
        )

    if order_code:
        query = query.filter(
            Order.order_code.ilike(f"%{order_code}%")
        )

    total = query.count()

    orders = (
        query.order_by(Order.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return orders, total


def update_order(
    db: Session,
    order_id: int,
    order_data: OrderUpdate,
) -> Order | None:
    order = get_order(db, order_id)

    if order is None:
        return None

    update_data = order_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    return order


def delete_order(
    db: Session,
    order_id: int,
) -> bool:
    order = get_order(db, order_id)

    if order is None:
        return False

    order.deleted_at = datetime.now()

    db.commit()

    return True


def restore_order(
    db: Session,
    order_id: int,
) -> Order | None:
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.deleted_at.is_not(None),
        )
        .first()
    )

    if order is None:
        return None

    order.deleted_at = None

    db.commit()
    db.refresh(order)

    return order

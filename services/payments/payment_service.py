from datetime import datetime

from sqlalchemy.orm import Session

from models.payments.payment import Payment
from schemas.payments.payment import PaymentCreate, PaymentUpdate


def create_payment(
    db: Session,
    payment_data: PaymentCreate,
) -> Payment:
    payment = Payment(
        payment_code=payment_data.payment_code,
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status=payment_data.status,
        transaction_reference=payment_data.transaction_reference,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_payment(
    db: Session,
    payment_id: int,
) -> Payment | None:
    return (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
            Payment.deleted_at.is_(None),
        )
        .first()
    )


def get_payments(
    db: Session,
    order_id: int | None = None,
    status: str | None = None,
    payment_method: str | None = None,
    payment_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Payment).filter(
        Payment.deleted_at.is_(None)
    )

    if order_id:
        query = query.filter(
            Payment.order_id == order_id
        )

    if status:
        query = query.filter(
            Payment.status.ilike(f"%{status}%")
        )

    if payment_method:
        query = query.filter(
            Payment.payment_method.ilike(
                f"%{payment_method}%"
            )
        )

    if payment_code:
        query = query.filter(
            Payment.payment_code.ilike(
                f"%{payment_code}%"
            )
        )

    total = query.count()

    payments = (
        query.order_by(Payment.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return payments, total


def update_payment(
    db: Session,
    payment_id: int,
    payment_data: PaymentUpdate,
) -> Payment | None:
    payment = get_payment(db, payment_id)

    if payment is None:
        return None

    update_data = payment_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)

    return payment


def delete_payment(
    db: Session,
    payment_id: int,
) -> bool:
    payment = get_payment(db, payment_id)

    if payment is None:
        return False

    payment.deleted_at = datetime.now()

    db.commit()

    return True


def restore_payment(
    db: Session,
    payment_id: int,
) -> Payment | None:
    payment = (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
            Payment.deleted_at.is_not(None),
        )
        .first()
    )

    if payment is None:
        return None

    payment.deleted_at = None

    db.commit()
    db.refresh(payment)

    return payment

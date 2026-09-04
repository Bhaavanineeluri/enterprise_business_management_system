from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.payments.payment import (
    PaymentCreate,
    PaymentListResponse,
    PaymentPatch,
    PaymentSingleResponse,
    PaymentUpdate,
)
from services.payments.payment_service import (
    create_payment,
    delete_payment,
    get_payment,
    get_payments,
    restore_payment,
    update_payment,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_api(
    payment_data: PaymentCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    payment = create_payment(db, payment_data)

    response.headers["Location"] = (
        f"/api/v1/payments/{payment.id}"
    )

    return {
        "success": True,
        "message": "Payment created successfully",
        "data": payment,
    }


@router.get(
    "",
    response_model=PaymentListResponse,
)
def get_payments_api(
    order_id: int | None = Query(default=None, gt=0),
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    payment_method: str | None = Query(default=None),
    payment_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    payments, total = get_payments(
        db,
        order_id=order_id,
        status=status_filter,
        payment_method=payment_method,
        payment_code=payment_code,
        offset=offset,
        limit=page_size,
    )

    pages = (
        (total + page_size - 1) // page_size
        if total
        else 0
    )

    return {
        "success": True,
        "message": "Payments retrieved successfully",
        "data": {
            "items": payments,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get(
    "/{payment_id}",
    response_model=PaymentSingleResponse,
)
def get_payment_api(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = get_payment(db, payment_id)

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return {
        "success": True,
        "message": "Payment retrieved successfully",
        "data": payment,
    }


@router.put(
    "/{payment_id}",
    response_model=PaymentSingleResponse,
)
def update_payment_api(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
):
    payment = update_payment(
        db,
        payment_id,
        payment_data,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return {
        "success": True,
        "message": "Payment updated successfully",
        "data": payment,
    }


@router.patch(
    "/{payment_id}",
    response_model=PaymentSingleResponse,
)
def patch_payment_api(
    payment_id: int,
    payment_data: PaymentPatch,
    db: Session = Depends(get_db),
):
    payment = update_payment(
        db,
        payment_id,
        payment_data,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return {
        "success": True,
        "message": "Payment partially updated successfully",
        "data": payment,
    }


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_payment_api(
    payment_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_payment(db, payment_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/{payment_id}/restore",
    response_model=PaymentSingleResponse,
)
def restore_payment_api(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = restore_payment(
        db,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted payment not found",
        )

    return {
        "success": True,
        "message": "Payment restored successfully",
        "data": payment,
    }

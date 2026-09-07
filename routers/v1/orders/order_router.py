from dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.orders.order import (
    OrderCreate,
    OrderListResponse,
    OrderPatch,
    OrderSingleResponse,
    OrderUpdate,
)
from services.orders.order_service import (
    create_order,
    delete_order,
    get_order,
    get_orders,
    restore_order,
    update_order,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=OrderSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order_api(
    order_data: OrderCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    order = create_order(db, order_data)

    response.headers["Location"] = (
        f"/api/v1/orders/{order.id}"
    )

    return {
        "success": True,
        "message": "Order created successfully",
        "data": order,
    }


@router.get(
    "",
    response_model=OrderListResponse,
)
def get_orders_api(
    customer_id: int | None = Query(default=None, gt=0),
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    order_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    orders, total = get_orders(
        db,
        customer_id=customer_id,
        status=status_filter,
        order_code=order_code,
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
        "message": "Orders retrieved successfully",
        "data": {
            "items": orders,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get(
    "/{order_id}",
    response_model=OrderSingleResponse,
)
def get_order_api(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return {
        "success": True,
        "message": "Order retrieved successfully",
        "data": order,
    }


@router.put(
    "/{order_id}",
    response_model=OrderSingleResponse,
)
def update_order_api(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
):
    order = update_order(
        db,
        order_id,
        order_data,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return {
        "success": True,
        "message": "Order updated successfully",
        "data": order,
    }


@router.patch(
    "/{order_id}",
    response_model=OrderSingleResponse,
)
def patch_order_api(
    order_id: int,
    order_data: OrderPatch,
    db: Session = Depends(get_db),
):
    order = update_order(
        db,
        order_id,
        order_data,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return {
        "success": True,
        "message": "Order partially updated successfully",
        "data": order,
    }


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order_api(
    order_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_order(db, order_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/{order_id}/restore",
    response_model=OrderSingleResponse,
)
def restore_order_api(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = restore_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted order not found",
        )

    return {
        "success": True,
        "message": "Order restored successfully",
        "data": order,
    }

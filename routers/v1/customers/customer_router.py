from dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.customers.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerPatch,
    CustomerResponse,
    CustomerSingleResponse,
    CustomerUpdate,
)
from services.customers.customer_service import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    restore_customer,
    update_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=CustomerSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_api(
    customer_data: CustomerCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    customer = create_customer(
        db,
        customer_data,
    )

    response.headers["Location"] = (
        f"/api/v1/customers/{customer.id}"
    )

    return {
        "success": True,
        "message": "Customer created successfully",
        "data": customer,
    }


@router.get(
    "",
    response_model=CustomerListResponse,
)
def get_customers_api(
    name: str | None = Query(
        default=None,
        description="Search customers by company name",
    ),
    email: str | None = Query(
        default=None,
        description="Search customers by email",
    ),
    customer_code: str | None = Query(
        default=None,
        description="Search customers by customer code",
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    customers, total = get_customers(
        db,
        name=name,
        email=email,
        customer_code=customer_code,
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
        "message": "Customers retrieved successfully",
        "data": {
            "items": customers,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get(
    "/{customer_id}",
    response_model=CustomerSingleResponse,
)
def get_customer_api(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = get_customer(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return {
        "success": True,
        "message": "Customer retrieved successfully",
        "data": customer,
    }


@router.put(
    "/{customer_id}",
    response_model=CustomerSingleResponse,
)
def update_customer_api(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = update_customer(
        db,
        customer_id,
        customer_data,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return {
        "success": True,
        "message": "Customer updated successfully",
        "data": customer,
    }


@router.patch(
    "/{customer_id}",
    response_model=CustomerSingleResponse,
)
def patch_customer_api(
    customer_id: int,
    customer_data: CustomerPatch,
    db: Session = Depends(get_db),
):
    customer = update_customer(
        db,
        customer_id,
        customer_data,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return {
        "success": True,
        "message": "Customer partially updated successfully",
        "data": customer,
    }


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer_api(
    customer_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_customer(
        db,
        customer_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/{customer_id}/restore",
    response_model=CustomerSingleResponse,
)
def restore_customer_api(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = restore_customer(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted customer not found",
        )

    return {
        "success": True,
        "message": "Customer restored successfully",
        "data": customer,
    }

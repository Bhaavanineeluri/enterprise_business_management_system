from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.products.product import (
    ProductCreate,
    ProductListResponse,
    ProductPatch,
    ProductSingleResponse,
    ProductUpdate,
)
from services.products.product_service import (
    create_product,
    delete_product,
    get_product,
    get_products,
    restore_product,
    update_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_api(
    product_data: ProductCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    product = create_product(db, product_data)

    response.headers["Location"] = (
        f"/api/v1/products/{product.id}"
    )

    return {
        "success": True,
        "message": "Product created successfully",
        "data": product,
    }


@router.get(
    "",
    response_model=ProductListResponse,
)
def get_products_api(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    product_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    products, total = get_products(
        db,
        name=name,
        category=category,
        brand=brand,
        product_code=product_code,
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
        "message": "Products retrieved successfully",
        "data": {
            "items": products,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get(
    "/{product_id}",
    response_model=ProductSingleResponse,
)
def get_product_api(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "success": True,
        "message": "Product retrieved successfully",
        "data": product,
    }


@router.put(
    "/{product_id}",
    response_model=ProductSingleResponse,
)
def update_product_api(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = update_product(
        db,
        product_id,
        product_data,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "success": True,
        "message": "Product updated successfully",
        "data": product,
    }


@router.patch(
    "/{product_id}",
    response_model=ProductSingleResponse,
)
def patch_product_api(
    product_id: int,
    product_data: ProductPatch,
    db: Session = Depends(get_db),
):
    product = update_product(
        db,
        product_id,
        product_data,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "success": True,
        "message": "Product partially updated successfully",
        "data": product,
    }


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_api(
    product_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_product(db, product_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/{product_id}/restore",
    response_model=ProductSingleResponse,
)
def restore_product_api(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = restore_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted product not found",
        )

    return {
        "success": True,
        "message": "Product restored successfully",
        "data": product,
    }

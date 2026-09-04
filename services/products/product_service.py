from datetime import datetime

from sqlalchemy.orm import Session

from models.products.product import Product
from schemas.products.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:
    product = Product(
        product_code=product_data.product_code,
        name=product_data.name,
        category=product_data.category,
        brand=product_data.brand,
        price=product_data.price,
        cost_price=product_data.cost_price,
        stock=product_data.stock,
        minimum_stock=product_data.minimum_stock,
        vendor_id=product_data.vendor_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_product(
    db: Session,
    product_id: int,
) -> Product | None:
    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.deleted_at.is_(None),
        )
        .first()
    )


def get_products(
    db: Session,
    name: str | None = None,
    category: str | None = None,
    brand: str | None = None,
    product_code: str | None = None,
    offset: int = 0,
    limit: int = 10,
):
    query = db.query(Product).filter(
        Product.deleted_at.is_(None)
    )

    if name:
        query = query.filter(
            Product.name.ilike(f"%{name}%")
        )

    if category:
        query = query.filter(
            Product.category.ilike(f"%{category}%")
        )

    if brand:
        query = query.filter(
            Product.brand.ilike(f"%{brand}%")
        )

    if product_code:
        query = query.filter(
            Product.product_code.ilike(f"%{product_code}%")
        )

    total = query.count()

    products = (
        query.order_by(Product.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return products, total


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
) -> Product | None:
    product = get_product(db, product_id)

    if product is None:
        return None

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int,
) -> bool:
    product = get_product(db, product_id)

    if product is None:
        return False

    product.deleted_at = datetime.now()

    db.commit()

    return True


def restore_product(
    db: Session,
    product_id: int,
) -> Product | None:
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.deleted_at.is_not(None),
        )
        .first()
    )

    if product is None:
        return None

    product.deleted_at = None

    db.commit()
    db.refresh(product)

    return product

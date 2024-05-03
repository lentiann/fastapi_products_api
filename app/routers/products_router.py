from typing import List

from fastapi import APIRouter

from app.repositories import products as products_repository
from app.schemas import schemas as schemas
from app.utils.database import SessionLocal
from app.utils.exceptions import ProductNotFound

router = APIRouter(
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    return products_repository.get_products(db, skip, limit)


@router.post("", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate):
    db = SessionLocal()
    return products_repository.create_product(db, product)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int):
    db = SessionLocal()
    product = products_repository.get_product(db, product_id)
    if product is None:
        raise ProductNotFound()
    return product


@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int):
    db = SessionLocal()
    return products_repository.delete_product(db, product_id)


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate):
    db = SessionLocal()
    return products_repository.update_product(db, product_id, product)

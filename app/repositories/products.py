from sqlalchemy.orm import Session

import app.schemas.schemas as schemas
import app.models.models as models


def get_product(db: Session, product_id: int):
    """
        select * from products where id = product_id
        limit 1
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
        select * from products
        limit 100
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    """
        insert into products (name, description, price)
        values (product.name, product.description, product.price)
    """
    # db_product = models.Product(name=product.name, description=product.description, price=product.price)
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    """
        update products
        set name = product.name, description = product.description, price = product.price
        where id = product_id
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """
        delete from products
        where id = product_id
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    return None

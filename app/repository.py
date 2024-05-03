from sqlalchemy.orm import Session
from . import models, schemas


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


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
        select * from users
        limit 100
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    """
        select * from users
        where id = user_id
        limit 1
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
        select * from users
        where username = username
        limit 1
    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
        insert into users (name, email, password)
        values (user.name, user.email, user.password)
    """

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    """
        update users
        set name = user.name, email = user.email, password = user.password
        where id = user_id
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
        delete from users
        where id = user_id
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

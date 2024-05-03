from sqlalchemy.orm import Session

import app.schemas.schemas as schemas
import app.models.models as models


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

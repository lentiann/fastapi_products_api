from datetime import timedelta
from typing import List, Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from app import schemas
import app.auth_jwt as authentication
from app.database import SessionLocal
import app.repository as repository

from app.exceptions import ProductNotFound

app = FastAPI()


@app.exception_handler(ProductNotFound)
async def product_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db = SessionLocal()
    user.password = authentication.get_password_hash(user.password)
    return repository.create_user(db, user)


@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate):
    db = SessionLocal()
    return repository.create_product(db, product)


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int):
    db = SessionLocal()
    product = repository.get_product(db, product_id)
    if product is None:
        raise ProductNotFound()
    return product


@app.get("/products", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    return repository.get_products(db, skip, limit)


@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int):
    db = SessionLocal()
    return repository.delete_product(db, product_id)


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate):
    db = SessionLocal()
    return repository.update_product(db, product_id, product)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authentication.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/items/")
def read_own_items(user: schemas.User = Depends(authentication.get_current_active_user)):
    return {"username": user.username, "email": user.email}

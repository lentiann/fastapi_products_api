from typing import List, Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app import schemas
from app.auth import fake_users_db, UserInDB, fake_hash_password, User, get_current_active_user
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


@app.get("/")
def home():
    return {"status": "ok"}


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
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

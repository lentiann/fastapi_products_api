from typing import List

from fastapi import FastAPI

from app import schemas
from app.database import SessionLocal
import app.repository as repository

app = FastAPI()


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
    return repository.get_product(db, product_id)


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

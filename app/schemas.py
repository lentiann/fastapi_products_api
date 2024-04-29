from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    description: str
    price: int

    @field_validator('price')
    def price_must_be_positive(cls, price):
        if price < 0:
            raise ValueError('price must be positive')
        return price


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

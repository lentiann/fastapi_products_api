import pytest
from pydantic import ValidationError

from app.schemas.schemas import ProductCreate


# @pytest.fixture
# def product():
#     return {"name": "Test Product", "description": "Test Description"}
#

def test_create_product_with_invalid_price():
    product = {"name": "Test Product", "description": "Test Description", "price": -1}
    # product["price"] = -1

    with pytest.raises(ValidationError):
        ProductCreate(**product)


def test_create_product_with_valid_price():
    product = {"name": "Test Product", "description": "Test Description", "price": 2}
    # product["price"] = 2
    print("Product: ", product)
    assert ProductCreate(**product)
    assert ProductCreate(**product).price == 2
    assert ProductCreate(**product).name == "Test Product"
    assert ProductCreate(**product).description == "Test Description"

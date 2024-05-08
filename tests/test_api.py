from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_product():
    product = {"name": "Product 1", "description": "Test Descripton", "price": 9.99}
    response = client.post("/products/", json=product)

    assert response.status_code == 200
    assert response.json()["name"] == product["name"]
    assert response.json()["description"] == product["description"]
    assert response.json()["price"] == product["price"]
    assert response.json()["id"] is not None

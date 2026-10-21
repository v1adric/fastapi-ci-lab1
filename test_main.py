from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_item_success():
    response = client.get("/api/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_get_item_not_found():
    response = client.get("/api/items/999")
    assert response.status_code == 404

def test_create_item():
    new_item = {"name": "Keyboard", "description": "Mechanical", "price": 85.0}
    response = client.post("/api/items", json=new_item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Keyboard"
    assert "id" in data

def test_delete_item():
    response = client.delete("/api/items/2")
    assert response.status_code == 204
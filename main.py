from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Items Management API",
    description="REST API для Лабораторної роботи №1 (CI/CD)",
    version="1.0.0"
)

# Модель даних
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# Збереження даних у пам'яті
db: dict[int, Item] = {
    1: Item(id=1, name="Laptop", description="Gaming Laptop", price=1200.0),
    2: Item(id=2, name="Mouse", description="Wireless Mouse", price=25.0)
}
current_id = 2

@app.get("/api/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def get_items():
    return list(db.values())

@app.get("/api/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    global current_id
    current_id += 1
    item.id = current_id
    db[current_id] = item
    return item

@app.put("/api/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, updated_item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item.id = item_id
    db[item_id] = updated_item
    return updated_item

@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return None
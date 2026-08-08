from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
     name: str
     price: float
     is_offer: bool | None = None

@app.get("/")
def get_root():
    return {"Hello": "World"}

@app.put("/items/{item_id}")
def put_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}



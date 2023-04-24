from typing import Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    """
    Get one item info.
    :param item_id: ID of the item.
    :param q: Arbitrary param.
    :return:
    """
    return {"item_id": item_id, "q": q}


@app.get("/items")
async def list_items():
    return [{"item_id": f"item_id_{i}", "q": i} for i in range(10)]


@app.post("/items", response_model=Item, response_model_exclude_unset=True)
async def create_item(item: Item):
    return item

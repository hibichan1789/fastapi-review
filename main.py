from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Annotated

app = FastAPI()

class Item(BaseModel):
    name:Annotated[str, Field(..., min_length=1)]
    description:Annotated[str|None, Field(default=None, max_length=100)]
    price:Annotated[float, Field(ge=0)]
    tags:Annotated[set[str], Field(default=set())]#setとして定義することでユニークな項目に代わる

@app.post("/items")
def create_item(item:Item):
    print(item)
    return item
from typing import Annotated

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

#Body has the same metadata parameters as Query and Path
@app.put("/items/{item_id}")
async def update_item(
        item_id: int,
        item: Item,
        user: User,
        importance: Annotated[int, Body(gt=0)]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# FastAPI expects this:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }


@app.put("/itemss/{item_id}")
async def update_item(
        item_id: int,
        item: Annotated[Item, Body(embed=True)]
):
    results = {"item_id": item_id, "item": item}
    return results

# In this case FastAPI will expect a body like:
#
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }
# instead of:
#
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }
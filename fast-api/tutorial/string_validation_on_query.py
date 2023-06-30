from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

#Query is used to do string validation on query parameters
@app.get("/items/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                alias="item-query",
                title="Query string",
                description="Query string for the items to search in the db",
                min_length=3,
                max_length=50,
                regex="^fixedquery$",
                deprecated=True
            )
        ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#This handles http://localhost:8000/items/?q=foo&q=bar
@app.get("/itemss")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
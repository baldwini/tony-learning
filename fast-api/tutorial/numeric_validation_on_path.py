from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

#Path can use all the same metadata parameters as for Query
#gt for Greater Than, ge for Greater Than or Equal To, etc for le, lt
@app.get("/items/{item_id}")
async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
        q: Annotated[str | None, Query(alias="item-query")],
        size: Annotated[float, Query(gt=0, lt=10.5)]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results

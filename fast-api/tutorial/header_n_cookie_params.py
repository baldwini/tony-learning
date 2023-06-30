from typing import Annotated
from fastapi import Cookie, FastAPI, Header

app = FastAPI()

#Cookie param usage
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

#Header param usage
@app.get("/itemss/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

@app.get("/itemsss/")
async def read_items(
        strange_header: Annotated[str | None, Header(convert_underscores=False)] = None
):
    return {"stranger_header": strange_header}

@app.get("/itemssss/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return{"X-Token values": x_token}

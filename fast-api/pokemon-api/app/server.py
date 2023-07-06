import json
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
poke_url = "https://pokeapi.co/api/v2/pokemon/"

client = httpx.AsyncClient(verify=False)


class Pokemon(BaseModel):
    name: str
    id: int


async def get_pokemon_from_api(poke_id: int):
    response = await client.get(poke_url + str(poke_id))
    return response


@app.get("/{poke_id}")
async def get_pokemon_by_id(poke_id: int) -> Pokemon:
    response = await get_pokemon_from_api(poke_id)
    pokemon = response.json()
    return Pokemon(id=poke_id, name=pokemon['forms'][0]['name'])

"""
    Pokemon Router API Endpoint
"""
from fastapi import APIRouter, Request, HTTPException
import redis

from app.models.pokemon_api_models import Pokemon

poke_url = "https://pokeapi.co/api/v2/pokemon/"

router = APIRouter()


class PokemonRouter:
    @router.get(
        path="/{poke_id}",
        response_model=Pokemon,
        description="Gets Pokemon from Redis",
    )
    async def get_pokemon_by_id(request: Request, poke_id: int) -> Pokemon:
        db: redis.Redis = request.state.redis_db
        response = db.get(poke_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Pokemon.parse_raw(response)

    @router.post(
        path="/{poke_id}",
        response_model=Pokemon,
        description="Creates new Pokemon in Redis by retrieving it from Pokeapi"
    )
    async def create_pokemon(request: Request, poke_id: int) -> Pokemon:
        if request.state.redis_db.get(poke_id) is not None:
            raise HTTPException(status_code=409, detail="Item already exists")
        response = await request.state.client.get(poke_url + str(poke_id))
        pokemon = response.json()
        pokemon_obj = Pokemon(id=poke_id, name=pokemon['forms'][0]['name'])
        request.state.redis_db.set(request.path_params['poke_id'], pokemon_obj.json())
        return pokemon_obj

    @router.delete(
        path="/{poke_id}",
        response_model=Pokemon,
        description="Deletes Pokemon in Redis"
    )
    async def delete_pokemon(request: Request, poke_id: int) -> Pokemon:
        db: redis.Redis = request.state.redis_db
        response = db.get(poke_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(poke_id)
        return Pokemon.parse_raw(response)

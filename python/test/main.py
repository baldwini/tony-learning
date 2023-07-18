import httpx
import asyncio

poke_url = "https://pokeapi.co/api/v2/pokemon/"
client = httpx.AsyncClient(verify=False)


async def fnc():
    resp = await client.get(poke_url+"2")
    print(resp)

asyncio.run(fnc())

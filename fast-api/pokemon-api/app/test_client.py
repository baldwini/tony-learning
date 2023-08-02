import httpx
import asyncio
import json
import random

async def main():
    async with httpx.AsyncClient(verify=False) as client:
        responses = []
        for i in range(100):
            poke_num = random.randint(1, 1000)
            response = await client.get("http://127.0.0.1:8000/" + str(poke_num))
            poke_obj = response.json()
            print(poke_obj['name'])
            responses.append(poke_obj)
        print(responses)

if __name__ == '__main__':
    asyncio.run(main())

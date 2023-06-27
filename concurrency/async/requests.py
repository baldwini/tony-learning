import asyncio
import httpx
import json
import time

start_time = time.time()
async def main():
    jokes = []
    async with httpx.AsyncClient(verify=False) as client:
        for number in range(0, 100):
            joke_url = "https://api.chucknorris.io/jokes/random"
            resp = await client.get(joke_url)
            joke = resp.json()
            jokes.append(
                {
                    'joke_id': number+1,
                    'joke': joke['value']
                }
            )
        json_file = open('./jokes.json', 'w')
        json.dump(jokes, json_file)

if __name__ == "__main__":
    asyncio.run(main())
    print(f"--- {time.time() - start_time} seconds ---")

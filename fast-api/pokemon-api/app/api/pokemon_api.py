import httpx
import uvicorn
import json
import redis
from fastapi import FastAPI, Request, Response

from app.routers import pokemon_router


class PokemonApi:
    def __init__(self):

        app = FastAPI(
            title="Pokemon API",
            description="Allows you to access Pokemon by ID.",
            version="1.0.0"
        )
        app.include_router(pokemon_router.router)
        self.uv_server = uvicorn.Server(
            uvicorn.Config(
                app=app,
                host="0.0.0.0",
                port=8000
            )
        )
        self.client = httpx.AsyncClient(verify=False)
        self.redis_db = redis.Redis(
            host='redis_db',
            port=6379,
            db=0
        )

        @app.on_event("startup")
        async def startup_event():
            print("Starting Up...")

        @app.middleware("http")
        async def pokemon_middleware(request: Request, call_next):
            request.state.client = self.client
            request.state.redis_db = self.redis_db
            response = await call_next(request)
            return response

            #Load response_body courtesy of https://stackoverflow.com/a/71883126
            #response_body = b""
            #async for chunk in response.body_iterator:
            #    response_body += chunk
            #print(f"response_body={response_body.decode()}")

            #Set response in Redis
            #self.r.set(request.path_params['poke_id'], response_body.decode())

            #return Response(content=response_body, status_code=response.status_code,
            #                headers=dict(response.headers), media_type=response.media_type)


if __name__ == "__main__":
    pokemon_api = PokemonApi()
    pokemon_api.uv_server.run()

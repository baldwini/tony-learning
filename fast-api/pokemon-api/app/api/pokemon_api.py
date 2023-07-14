import httpx
import uvicorn
import redis
from fastapi import FastAPI, Request

from app.routers import pokemon_router
from app.rabbitmq import rabbitmq_connection_manager


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
        self.rmq_conn_mgr = rabbitmq_connection_manager.RabbitMQConnectionManager()

        @app.on_event("startup")
        async def startup_event():
            print("Creating RabbitMQ Manager Asynchronously...")
            await self.rmq_conn_mgr.create()

        @app.middleware("http")
        async def pokemon_middleware(request: Request, call_next):
            request.state.client = self.client
            request.state.redis_db = self.redis_db
            request.state.rmq = self.rmq_conn_mgr
            response = await call_next(request)
            return response


if __name__ == "__main__":
    pokemon_api = PokemonApi()
    pokemon_api.uv_server.run()

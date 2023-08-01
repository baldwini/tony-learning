"""
    Pokemon Router API Endpoint
"""
from fastapi import APIRouter, Request, HTTPException
from aiormq.connection import AbstractChannel
from aiormq.abc import DeliveredMessage
from typing import Coroutine
import redis
from uuid import uuid4
import asyncio
import aiormq

from app.models.pokemon_api_models import Pokemon, Transaction, ApiResponse
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager

poke_url = "https://pokeapi.co/api/v2/pokemon/"

router = APIRouter()


class PokemonRouter:

    @router.get(
        path="/{poke_id}",
        response_model=Pokemon,
        description="Submits Get Request to Rabbit",
    )
    async def get_pokemon_by_id(request: Request, poke_id: int) -> Pokemon:
        rmq: RabbitMQConnectionManager = request.state.rmq
        ch: AbstractChannel = rmq.channel

        correlation_id = str(uuid4())
        future = asyncio.get_event_loop().create_future()

        request.state.get_futures[correlation_id] = future

        await ch.basic_publish(
            body=str(poke_id).encode('ASCII'),
            exchange=rmq.pokemon_exchange,
            routing_key='get',
            properties=aiormq.spec.Basic.Properties(
                content_type='text/plain',
                correlation_id=correlation_id,
                reply_to='get_callback_queue',
            )
        )

        await ch.basic_consume(queue='get_callback_queue', consumer_callback=request.state.on_get_response, no_ack=True)

        return Pokemon.parse_raw(await future)

    @router.post(
        path="/{poke_id}",
        response_model=None,
        description="Produces set command in RMQ to deliver to Database Microservice"
    )
    async def publish_pokemon_set(
            request: Request,
            poke_id: int,
            trace_id: str | None = None,
            transaction_id: str | None = None,
    ):
        response = await request.state.client.get(poke_url + str(poke_id))
        pokemon = response.json()

        if not trace_id:
            trace_id = str(uuid4())
        if not transaction_id:
            transaction_id = str(uuid4())

        pokemon_obj = Pokemon(id=poke_id, name=pokemon['forms'][0]['name'])

        transaction_obj = Transaction(trace_id=trace_id, transaction_id=transaction_id, pokemon=pokemon_obj)

        rmq: RabbitMQConnectionManager = request.state.rmq
        ch: AbstractChannel = rmq.channel
        await ch.basic_publish(
            exchange=rmq.pokemon_exchange,
            routing_key='set',
            body=transaction_obj.json().encode('ASCII')
        )

    @router.delete(
        path="/{poke_id}",
        response_model=None,
        description="Produces delete command in RMQ to send to Database Microservice"
    )
    async def publish_pokemon_delete(
            request: Request,
            poke_id: int,
            trace_id: int | None = None,
            transaction_id: int | None = None,
    ):
        if not trace_id:
            trace_id = str(uuid4())
        if not transaction_id:
            transaction_id = str(uuid4())

        rmq: RabbitMQConnectionManager = request.state.rmq
        ch: AbstractChannel = rmq.channel

        pokemon_obj: Pokemon = Pokemon(id=poke_id)
        transaction_obj: Transaction = Transaction(trace_id=trace_id, transaction_id=transaction_id, pokemon=pokemon_obj)

        await ch.basic_publish(
            exchange=rmq.pokemon_exchange,
            routing_key='delete',
            body=transaction_obj.json().encode('ASCII')
        )

    @router.get(
        path="/redis/{poke_id}",
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
        path="/redis/{poke_id}",
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
        path="/redis/{poke_id}",
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

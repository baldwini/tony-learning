import aiormq
from aiormq import Connection
from aiormq.connection import AbstractChannel
from typing import Optional


class RabbitMQConnectionManager:

    def __init__(self):
        self.pokemon_exchange: str = 'pokemon_exchange'
        self.kafka_exchange: str = 'kafka_exchange'
        self.connection: Optional[Connection] = None
        self.channel: Optional[AbstractChannel] = None

    async def create(self):
        self.connection = await aiormq.connect(url="amqp://guest:guest@rmq/")
        self.channel = await self.connection.channel()

    async def create_pokemon_exchange(self):
        await self.channel.exchange_declare(
            exchange=self.pokemon_exchange,
            exchange_type='direct'
        )

    async def create_kafka_exchange(self):
        await self.channel.exchange_declare(
            exchange=self.kafka_exchange,
            exchange_type='x-consistent-hash'
        )

    async def define_pokemon_queue(self, command: str):
        queue = await self.channel.queue_declare(
            queue=command+'_queue',
        )

        await self.channel.queue_bind(
            queue=queue.queue,
            exchange=self.pokemon_exchange,
            routing_key=command
        )

    async def define_kafka_queue(self, weight: int):
        queue = await self.channel.queue_declare(
            queue='kafka_queue'
        )

        await self.channel.queue_bind(
            queue=queue.queue,
            exchange=self.kafka_exchange,
            routing_key=str(weight)
        )

    async def define_callback_queue(self, command: str):
        callback_queue = await self.channel.queue_declare(
            queue=command+'_callback_queue',
        )
        await self.channel.queue_bind(
            queue=callback_queue.queue,
            exchange=self.pokemon_exchange,
            routing_key=command+'_callback'
        )

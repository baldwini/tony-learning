import aiormq
from aiormq import Connection
from aiormq.connection import AbstractChannel
from typing import Optional


class RabbitMQConnectionManager:

    def __init__(self):
        self.exchange: str = 'pokemon_exchange'
        self.connection: Optional[Connection] = None
        self.channel: Optional[AbstractChannel] = None

    async def create(self):
        self.connection = await aiormq.connect(url="amqp://guest:guest@rmq/")
        self.channel = await self.connection.channel()

        await self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct'
        )

    async def define_queue(self, command: str):
        queue = await self.channel.queue_declare(
            queue=command+'_queue',
        )

        await self.channel.queue_bind(
            queue=queue.queue,
            exchange=self.exchange,
            routing_key=command
        )

    async def define_callback_queue(self, command: str):
        callback_queue = await self.channel.queue_declare(
            queue=command+'_callback_queue',
        )
        await self.channel.queue_bind(
            queue=callback_queue.queue,
            exchange=self.exchange,
            routing_key=command+'_callback'
        )

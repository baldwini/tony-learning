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
        self.connection = await aiormq.connect(url="amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()

        await self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct'
        )

        commands = ['set', 'delete']
        for command in commands:
            await self.channel.queue_declare(
                queue=command + '_queue',
                exclusive=True,
            )

            await self.channel.queue_bind(
                queue=command + '_queue',
                exchange=self.exchange,
                routing_key=command
            )

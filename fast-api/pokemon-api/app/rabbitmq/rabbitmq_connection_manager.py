import aiormq
from aiormq import Connection
from aiormq.connection import AbstractChannel


class RabbitMQConnectionManager:

    def __init__(self):
        self.pokemon_exchange: str = 'pokemon_exchange'
        self.kafka_exchange: str = 'kafka_exchange'
        self.kafka_queue_amount: int = 3
        self.connection: Connection | None = None
        self.channel: AbstractChannel | None = None

    async def create(self):
        self.connection = await aiormq.connect(url="amqp://guest:guest@127.0.0.1/")
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
        for i in range(self.kafka_queue_amount):
            queue = await self.channel.queue_declare(
                queue='kafka_queue_' + str(i)
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

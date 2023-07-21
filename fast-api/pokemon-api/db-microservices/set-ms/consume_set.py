from redis import Redis
from aiormq.abc import DeliveredMessage
import asyncio

from app.models.pokemon_api_models import Pokemon
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager

rmq = RabbitMQConnectionManager()
redis_db: Redis = Redis(
    host='redis_db',
    port=6379,
    db=0
)


async def callback(message: DeliveredMessage):
    pokemon = Pokemon.parse_raw(message.body)
    redis_db.set(pokemon.id, pokemon.json())


async def main():
    await rmq.create()
    await rmq.define_queue('set')
    await rmq.channel.basic_qos(prefetch_count=1)
    await rmq.channel.basic_consume(queue='set_queue', consumer_callback=callback, no_ack=True)

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()

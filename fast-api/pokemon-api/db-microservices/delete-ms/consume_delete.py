from redis import Redis
from aiormq.types import DeliveredMessage
import asyncio

from app.models.pokemon_api_models import Pokemon
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager

rmq = RabbitMQConnectionManager()
redis_db: Redis = Redis(
    host='redis_db',
    port=6379,
    db=0
)


async def callback(body: DeliveredMessage):
    poke_id = body.body.decode('ASCII')
    redis_db.delete(poke_id)


async def main():
    await rmq.create()
    await rmq.define_queue('delete')
    await rmq.channel.basic_qos(prefetch_count=100)
    await rmq.channel.basic_consume(queue='delete_queue', consumer_callback=callback, no_ack=True)

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()

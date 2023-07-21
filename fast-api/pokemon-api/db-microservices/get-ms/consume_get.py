from redis import Redis
import aiormq
from aiormq.abc import DeliveredMessage
import asyncio

from app.models.pokemon_api_models import Pokemon
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager

rmq = RabbitMQConnectionManager()
redis_db: Redis = Redis(
    host='127.0.0.1',
    port=6379,
    db=0
)


async def callback(message: DeliveredMessage):
    poke_id = message.body.decode()

    print(poke_id + "  we in get message")

    response: bytes = redis_db.get(poke_id)

    await message.channel.basic_publish(
        response, routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),
    )
    await message.channel.basic_ack(message.delivery.delivery_tag)
    print('Request complete')


async def main():
    await rmq.create()
    await rmq.define_queue('get')
    await rmq.define_callback_queue('get')
    await rmq.channel.basic_qos(prefetch_count=1)
    await rmq.channel.basic_consume(queue='get_queue', consumer_callback=callback)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

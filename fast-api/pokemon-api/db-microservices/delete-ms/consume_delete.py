from redis import Redis
from aiormq.abc import DeliveredMessage
import asyncio

from app.models.pokemon_api_models import Pokemon, ApiResponse, Transaction
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager


rmq = RabbitMQConnectionManager()
redis_db: Redis = Redis(
    host='localhost',
    port=6379,
    db=0
)


async def callback(message: DeliveredMessage):
    transaction: Transaction = Transaction.parse_raw(message.body)
    pokemon: Pokemon = transaction.pokemon
    status_code: str = "200"
    error_message: str
    response: ApiResponse

    if not redis_db.get(pokemon.id):
        status_code = "404"
        error_message = "Pokemon not found"
        response = ApiResponse(trace_id=transaction.trace_id, status_code=status_code, message=error_message)

    else:
        redis_db.delete(pokemon.id)
        response = ApiResponse(trace_id=transaction.trace_id, status_code=status_code, message=pokemon.json())

    return response


async def main():
    await rmq.create()
    await rmq.create_pokemon_exchange()
    await rmq.define_pokemon_queue(command='delete')
    await rmq.create_kafka_exchange()
    await rmq.define_kafka_queue(weight=1)
    await rmq.channel.basic_qos(prefetch_count=1)
    await rmq.channel.basic_consume(queue='delete_queue', consumer_callback=callback, no_ack=True)

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()

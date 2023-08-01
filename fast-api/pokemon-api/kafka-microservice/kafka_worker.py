import asyncio
from app.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager
from app.kafka.kafka_lib import KafkaProducer


class PokemonKafkaWorker:
    def __init__(self):
        self.rmq_conn_mgr: RabbitMQConnectionManager = RabbitMQConnectionManager()
        self.pokemon_kafka_producer: KafkaProducer = KafkaProducer()

    async def startup(self) -> None:
        await self.rmq_conn_mgr.create()
        await self.rmq_conn_mgr.create_kafka_exchange()
        await self.rmq_conn_mgr.define_kafka_queue(1)

    async def consume_message(self, count: int) -> None:
        await self.rmq_conn_mgr.channel.basic_qos(prefetch_count=1)
        await self.rmq_conn_mgr.channel.basic_consume(queue='kafka_queue_'+str(count), consumer_callback=self.pokemon_kafka_producer.rmq_callback_to_forward)


async def main() -> None:
    pkw: PokemonKafkaWorker = PokemonKafkaWorker()
    await pkw.startup()
    print("here1")
    for count in range(pkw.rmq_conn_mgr.kafka_queue_amount):
        await pkw.consume_message(count)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

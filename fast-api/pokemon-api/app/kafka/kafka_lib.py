import json
import avro.schema
from confluent_kafka.avro import AvroProducer
from app.models.avro_datamodels import (pokemon_avro_schema, PokemonAvroSchema)
from aiormq.abc import DeliveredMessage


class KafkaProducer:
    def __init__(self):
        self.pokemon_conf: dict = {
            "bootstrap.servers": "[redacted]",
            "schema.registry.url": "[redacted]",
        }
        self.pokemon_avro_schema: str = json.dumps(pokemon_avro_schema)
        self.pokemon_avro_value_schema: avro.schema.RecordSchema = avro.schema.parse(self.pokemon_avro_schema)
        self.pokemon_kafka_producer: AvroProducer = AvroProducer(config=self.pokemon_conf, default_value_schema=self.pokemon_avro_schema)

    async def send_kafka_message(self, topic: str, value: dict, value_schema: avro.schema.RecordSchema) -> None:
        self.pokemon_kafka_producer.produce(
            topic=topic,
            value=value,
            value_schema=value_schema,
        )
        self.pokemon_kafka_producer.poll(2)

    async def rmq_callback_to_forward(self, message: DeliveredMessage) -> None:
        await self.send_kafka_message(topic='ian_test', value=json.loads(message.body), value_schema=self.pokemon_avro_value_schema)
        await message.channel.basic_ack(message.delivery.delivery_tag)

import json
import secrets

import avro.schema
from confluent_kafka import Consumer, Message
from confluent_kafka.avro import AvroProducer
from avro.io import DatumReader, BinaryDecoder
from secrets import SystemRandom
from io import BytesIO
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


class KafkaConsumer:
    def __init__(self):
        self.secrets: SystemRandom = secrets.SystemRandom()
        self.pokemon_conf: dict = {
            "bootstrap.servers": "[redacted]",
            "group.id": f"groupid-{self.secrets.randrange(start=1, stop=100)}"
        }
        self.pokemon_avro_schema: str = json.dumps(pokemon_avro_schema)
        self.pokemon_avro_value_schema: avro.schema.Schema = avro.schema.parse(self.pokemon_avro_schema)
        self.pokemon_kafka_consumer: Consumer = Consumer(self.pokemon_conf)

    def decoder(self, msg_value) -> object:
        """
        deserialize avro message
        :param msg_value:
        :return:
        """

        schema: avro.schema.Schema = avro.schema.parse(self.pokemon_avro_schema)
        reader: DatumReader = DatumReader(schema)
        message_bytes: BytesIO = BytesIO(msg_value)
        message_bytes.seek(5)
        decoder: BinaryDecoder = BinaryDecoder(message_bytes)
        event_dict: object = reader.read(decoder)
        return event_dict

    def start_consume(self) -> None:
        self.pokemon_kafka_consumer.subscribe(topics=["ian_test"])
        while True:
            msg: Message | None = self.pokemon_kafka_consumer.poll(timeout=1.0)
            if msg is None:
                print("No message found from poll")
                continue
            event_dict = self.decoder(msg.value())
            print(event_dict)

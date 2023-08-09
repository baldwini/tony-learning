from app.kafka.kafka_lib import KafkaConsumer


class PokemonKafkaConsumerWorker:
    def __init__(self):
        self.pokemon_kafka_consumer: KafkaConsumer = KafkaConsumer()


if __name__ == "__main__":
    pkcw: PokemonKafkaConsumerWorker = PokemonKafkaConsumerWorker()
    pkcw.pokemon_kafka_consumer.start_consume()

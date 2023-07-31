from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel


@dataclass
class Pokemon(AvroModel):
    name: str = field(metadata={"doc": "Pokemon Name"})
    id: int = field(metadata={"doc": "Pokemon ID"})


@dataclass
class Transaction(AvroModel):
    """
    Schema used for Transaction Information
    """
    trace_id: str = field(metadata={"doc": "Trace ID for the Transaction"})
    transaction_id: str = field(metadata={"doc": "Transaction ID for the Transaction"})
    pokemon: Pokemon = field(metadata={"doc": "Pokemon Object storing poke_id and name"})


@dataclass
class PokemonAvroSchema(AvroModel):
    """
    Schema used for Pokemon API
    """
    transaction: Transaction = field(metadata={"doc": "Transaction object storing trace_id, transaction_id, and Pokemon information"})
    status_code: str = field(metadata={"doc": "PokemonAPI Transaction Status Code"})
    message: str = field(metadata={"doc": "PokemonAPI Transaction Status Message"})


pokemon_avro_schema = {
    "type": "record",
    "name": "PokemonAvroSchema",
    "fields": [
        {
            "doc": "Transaction object storing trace_id, transaction_id, and Pokemon information",
            "name": "transaction",
            "type": {
                "type": "record",
                "name": "Transaction",
                "fields": [
                    {
                        "doc": "Trace ID for the Transaction",
                        "name": "trace_id",
                        "type": "string"
                    },
                    {
                        "doc": "Transaction ID for the Transaction",
                        "name": "transaction_id",
                        "type": "string"
                    },
                    {
                        "doc": "Pokemon Object storing poke_id and name",
                        "name": "pokemon",
                        "type": {
                            "type": "record",
                            "name": "Pokemon",
                            "fields": [
                                {
                                    "doc": "Pokemon Name",
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "doc": "Pokemon ID",
                                    "name": "id",
                                    "type": "long"
                                }
                            ]
                        }
                    }
                ],
                "doc": "Schema used for Transaction Information"
            }
        },
        {
            "doc": "PokemonAPI Transaction Status Code",
            "name": "status_code",
            "type": "string"
        },
        {
            "doc": "PokemonAPI Transaction Status Message",
            "name": "message",
            "type": "string"
        }
    ],
    "doc": "Schema used for Pokemon API"
}


# if __name__ == "__main__":
#     print(PokemonAvroSchema.avro_schema())

from pydantic import BaseModel


class Pokemon(BaseModel):
    name: str | None
    id: int


class Transaction(BaseModel):
    trace_id: str
    transaction_id: str
    pokemon: Pokemon


class ApiResponse(BaseModel):
    transaction: Transaction
    status_code: str
    message: str

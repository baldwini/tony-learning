from pydantic import BaseModel


class Pokemon(BaseModel):
    name: str
    id: int


class Transaction(BaseModel):
    trace_id: str
    pokemon: Pokemon

class ApiResponse(BaseModel):
    trace_id: str
    status_code: str
    message: str

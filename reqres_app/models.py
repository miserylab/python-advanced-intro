from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(frozen=True)
    name: str
    email: str


class Resource(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str

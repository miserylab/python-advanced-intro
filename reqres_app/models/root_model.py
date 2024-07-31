from pydantic import BaseModel


class Root(BaseModel):
    message: str

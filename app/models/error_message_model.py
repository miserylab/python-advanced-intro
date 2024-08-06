from pydantic import BaseModel


class BasicErrorResponse(BaseModel):
    detail: str


class ErrorDetail(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: str


class ErrorResponse(BaseModel):
    detail: list[ErrorDetail]

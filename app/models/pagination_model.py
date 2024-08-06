from pydantic import BaseModel

from app.models.user_model import User


class PaginationResponse(BaseModel):
    items: list[User]
    total: int
    page: int
    size: int
    pages: int

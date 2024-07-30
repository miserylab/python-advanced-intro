from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from reqres_app.database import users
from reqres_app.models.user_model import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
async def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User ID is invalid")
    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", status_code=HTTPStatus.OK)
async def get_users() -> Page[User]:
    disable_installed_extensions_check()
    # TODO use extension "fastapi_pagination.ext.sqlmodel" instead of default 'paginate' implementation.
    return paginate(users.get_users())


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User ID is invalid")
    user_entry = users.get_user(user_id)
    if user_entry is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int) -> None:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User ID is invalid")
    user_entry = users.get_user(user_id)
    if user_entry is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    users.delete_user(user_id)

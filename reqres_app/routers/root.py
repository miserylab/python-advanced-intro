from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
def get_root():
    return {"message": "Welcome to your FastAPI microservice!"}

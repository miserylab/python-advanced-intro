from http import HTTPStatus

from fastapi import APIRouter

from reqres_app.database.engine import check_availability
from reqres_app.models.app_status import AppStatus

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    return AppStatus(database=check_availability())

from app_tests.utils.config import Config


class Urls:
    def __init__(self, url=None):
        self._url = url or Config.app_url

    path_api: dict[str, str] = {
        "users": "/api/users/",
        "status": "/status",
    }

    def api_url(self, type_url: str) -> str:
        return f"{self._url}{self.path_api[type_url]}"

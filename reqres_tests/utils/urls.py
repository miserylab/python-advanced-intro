class Urls:
    def __init__(self, url=None):
        self.url = url

    path_api: dict[str, str] = {
        "users": "/api/users/",
        "status": "/status",
    }

    def api_url(self, type_url: str) -> str:
        return f"{self.path_api[type_url]}"

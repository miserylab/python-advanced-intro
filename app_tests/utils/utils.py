class Utils:
    @staticmethod
    def get_pages_in_pagination(total, size) -> int:
        return -(-total // size)

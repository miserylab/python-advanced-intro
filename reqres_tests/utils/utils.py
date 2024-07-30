from faker import Faker


class Utils:
    @staticmethod
    def get_pages_in_pagination(total, size) -> int:
        return -(-total // size)


class TestData:
    @staticmethod
    def get_test_user_data():
        faker = Faker("pt_BR")
        return {"id": 1, "name": faker.name(), "email": faker.email()}

    @staticmethod
    def get_test_user_data_for_update():
        faker = Faker("pt_BR")
        return {"id": 1, "name": faker.name(), "email": faker.email()}

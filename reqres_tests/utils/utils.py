from faker import Faker


class Utils:
    @staticmethod
    def get_pages_in_pagination(total, size) -> int:
        return -(-total // size)


class TestData:
    @staticmethod
    def get_test_user_data():
        faker = Faker("pt_BR")
        return {"email": faker.email(), "first_name": faker.first_name(), "last_name": faker.last_name(), "avatar": faker.image_url()}

    @staticmethod
    def get_test_user_data_for_update():
        faker = Faker("pt_BR")
        return {"email": faker.email(), "first_name": faker.first_name(), "last_name": faker.last_name(), "avatar": faker.image_url()}

    @staticmethod
    def get_test_user_data_invalid_email():
        faker = Faker("pt_BR")
        return {"email": faker.name, "first_name": faker.first_name(), "last_name": faker.last_name(), "avatar": faker.image_url()}

    @staticmethod
    def get_test_user_data_invalid_avatar():
        faker = Faker("pt_BR")
        return {"email": faker.email(), "first_name": faker.first_name(), "last_name": faker.last_name(), "avatar": faker.name}

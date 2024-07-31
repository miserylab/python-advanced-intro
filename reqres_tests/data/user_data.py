from faker import Faker


class UserData:
    USER_NOT_FOUND = "User not found"
    INVALID_USER_ID = "User ID is invalid"
    INVALID_USER_ID_TYPE = "Input should be a valid integer, unable to parse string as an integer"
    METHOD_NOT_ALLOWED = "Method Not Allowed"


class TestData:
    @staticmethod
    def get_test_user_data():
        faker = Faker("pt_BR")
        return {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        }

    @staticmethod
    def get_test_user_data_for_update():
        faker = Faker("pt_BR")
        return {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        }

    @staticmethod
    def get_test_user_data_invalid_email():
        faker = Faker("pt_BR")
        return {
            "email": faker.name,
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        }

    @staticmethod
    def get_test_user_data_invalid_avatar():
        faker = Faker("pt_BR")
        return {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.name,
        }

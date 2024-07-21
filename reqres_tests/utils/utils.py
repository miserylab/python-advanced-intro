from faker import Faker


class TestData:
    def __init__(self):
        self.faker = Faker("pt_BR")
        self.test_user_data_to_create = [{"id": 1, "name": self.faker.name(), "email": self.faker.email()}]
        self.update_user_data_to_create = [{"id": 1, "name": self.faker.name(), "email": self.faker.email()}]

    def get_test_user_data(self):
        return self.test_user_data_to_create[0]

    def get_test_user_data_for_update(self):
        return self.update_user_data_to_create[0]

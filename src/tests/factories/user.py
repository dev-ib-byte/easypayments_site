from datetime import datetime

import factory

from domain.entities.user import User
from infrastructure.enum import RoleEnum


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyAttribute(lambda o: f"user{o.id}@example.com")
    role = RoleEnum.USER
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    registration_date = factory.LazyFunction(datetime.now)
    posts = factory.List([])

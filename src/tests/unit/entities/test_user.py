from domain.entities.user import User
from infrastructure.enum import RoleEnum
from tests.factories.user import UserFactory


def test_change_role(user: User = UserFactory()) -> None:
    user.change_role(RoleEnum.USER)
    assert user.role == RoleEnum.USER

    user.change_role(RoleEnum.ADMIN)
    assert user.role == RoleEnum.ADMIN

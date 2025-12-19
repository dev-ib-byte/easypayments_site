from datetime import datetime
from typing import Optional

from src.domain.entities.entity import Entity


class User(Entity):
    def __init__(
        self,
        id: Optional[int] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[str] = None,
        registration_date: Optional[datetime] = datetime.now(),
    ) -> None:
        super().__init__(id)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.registration_date = registration_date

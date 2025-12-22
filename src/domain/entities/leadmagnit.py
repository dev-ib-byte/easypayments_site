from datetime import datetime

from src.domain.entities.entity import Entity


class LeadMagnit(Entity):
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        email: str | None = None,
        comment: str | None = None,
        replay: int = 0,
        active: bool = False,
        created_at: datetime | None = None,
    ) -> None:
        super().__init__(id)

        self.name = name
        self.email = email
        self.comment = comment
        self.replay = replay
        self.active = active
        self.created_at = created_at or datetime.now()

from src.domain.entities.entity import Entity


class TelegramPush(Entity):
    def __init__(
        self,
        id: int | None = None,
        chat_id: str | None = None,
        send: bool = True,
        error: bool = False,
        easypay_online: bool = False,
        consult: bool = False,
        buy_account: bool = False,
    ) -> None:
        super().__init__(id)

        self.chat_id = chat_id
        self.send = send
        self.error = error
        self.easypay_online = easypay_online
        self.consult = consult
        self.buy_account = buy_account

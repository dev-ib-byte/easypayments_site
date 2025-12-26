from src.domain.entities.telegram_push import TelegramPush
from src.infrastructure.models.alchemy.forms import TelegramPush as TelegramPushModel
from src.infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from src.infrastructure.repositories.interfaces.base import ModelRepository


class SqlAlchemyTelegramPushRepository(
    SqlAlchemyModelRepository[TelegramPush], ModelRepository
):
    MODEL = TelegramPushModel
    ENTITY = TelegramPush

    def convert_to_entity(self, model: TelegramPushModel) -> TelegramPush:
        return TelegramPush(
            id=model.id,
            chat_id=model.chat_id,
            send=model.send,
            error=model.error,
            easypay_online=model.easypay_online,
            consult=model.consult,
            buy_account=model.buy_account,
        )

    def convert_to_model(self, entity: TelegramPush) -> TelegramPushModel:
        return TelegramPushModel(
            chat_id=entity.chat_id,
            send=entity.send,
            error=entity.error,
            easypay_online=entity.easypay_online,
            consult=entity.consult,
            buy_account=entity.buy_account,
        )

from src.domain.entities.comment import Comment
from src.infrastructure.models.alchemy.forms import CommentOnline as CommentOnlineModel
from src.infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from src.infrastructure.repositories.interfaces.base import ModelRepository


class SqlAlchemyCommentsRepository(SqlAlchemyModelRepository[Comment], ModelRepository):
    MODEL = CommentOnlineModel
    ENTITY = Comment

    def convert_to_entity(self, model: CommentOnlineModel) -> Comment:
        return Comment(
            id=model.id,
            name=model.name,
            email=model.email,
            comment=model.comment,
            replay=model.replay,
            active=model.active,
            created_at=model.created_at,
        )

    def convert_to_model(self, entity: Comment) -> CommentOnlineModel:
        return CommentOnlineModel(
            name=entity.name,
            email=entity.email,
            comment=entity.comment,
            replay=entity.replay,
            active=entity.active,
        )

from src.domain.entities.form_order import FormOrder as FormOrderEntity
from src.infrastructure.models.alchemy.forms import FormOrder as FormOrderModel
from src.infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from src.infrastructure.repositories.interfaces.base import ModelRepository


class SqlAlchemyFormOrderRepository(
    SqlAlchemyModelRepository[FormOrderEntity],
    ModelRepository,
):
    MODEL = FormOrderModel
    ENTITY = FormOrderEntity

    def convert_to_entity(self, model: FormOrderModel) -> FormOrderEntity:
        return FormOrderEntity(
            id=model.id,
            form=model.form,
            telegram=model.telegram,
            email=model.email,
            phone=model.phone,
            description=model.description,
            comment=model.comment,
            link=model.link,
            theme_request=model.theme_request,
            promocode=model.promocode,
            url_form=model.url_form,
            utm_source=model.utm_source,
            utm_medium=model.utm_medium,
            utm_campaign=model.utm_campaign,
            utm_content=model.utm_content,
            created=model.created_at,
        )

    def convert_to_model(self, entity: FormOrderEntity) -> FormOrderModel:
        return FormOrderModel(
            form=entity.form,
            telegram=entity.telegram,
            email=entity.email,
            phone=entity.phone,
            description=entity.description,
            comment=entity.comment,
            link=entity.link,
            theme_request=entity.theme_request,
            promocode=entity.promocode,
            url_form=entity.url_form,
            utm_source=entity.utm_source,
            utm_medium=entity.utm_medium,
            utm_campaign=entity.utm_campaign,
            utm_content=entity.utm_content,
        )

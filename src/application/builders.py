from typing import Any

from src.application.constants import (
    UTM_CAMPAIGN_FIELD_ID,
    UTM_CAMPAIGN_FIELD_ID_CONTACT,
    UTM_CONTENT_FIELD_ID,
    UTM_CONTENT_FIELD_ID_CONTACT,
    UTM_MEDIUM_FIELD_ID,
    UTM_MEDIUM_FIELD_ID_CONTACT,
    UTM_SOURCE_FIELD_ID,
    UTM_SOURCE_FIELD_ID_CONTACT,
)
from src.domain.entities.form_order import FormOrder


def build_lead_data(entity: FormOrder, pipeline_id: int) -> list[dict[str, Any]]:
    return [
        {
            "name": entity.form,
            "pipeline_id": pipeline_id,
            "created_by": 0,
            "custom_fields_values": [
                {
                    "field_id": 163965,
                    "values": [{"value": entity.form}],
                },
                {
                    "field_id": 163967,
                    "values": [{"value": str(entity.telegram)}],
                },
                {
                    "field_id": 163969,
                    "values": [{"value": str(entity.email)}],
                },
                {
                    "field_id": 163971,
                    "values": [{"value": entity.phone}],
                },
                {
                    "field_id": 163975,
                    "values": [{"value": entity.comment}],
                },
                {
                    "field_id": 163977,
                    "values": [{"value": entity.description}],
                },
                {
                    "field_id": 163979,
                    "values": [{"value": entity.url_form}],
                },
                {
                    "field_id": UTM_SOURCE_FIELD_ID,
                    "values": [{"value": entity.utm_source}],
                },
                {
                    "field_id": UTM_MEDIUM_FIELD_ID,
                    "values": [{"value": entity.utm_medium}],
                },
                {
                    "field_id": UTM_CAMPAIGN_FIELD_ID,
                    "values": [{"value": entity.utm_campaign}],
                },
                {
                    "field_id": UTM_CONTENT_FIELD_ID,
                    "values": [{"value": entity.utm_content}],
                },
            ],
        }
    ]


def build_contact_data(entity: FormOrder) -> list[dict[str, Any]]:
    return [
        {
            "name": entity.email,
            "custom_fields_values": [
                {
                    "field_id": 141395,
                    "values": [{"value": entity.email}],
                },
                {
                    "field_id": 141393,
                    "values": [{"value": entity.phone}],
                },
                {
                    "field_id": UTM_SOURCE_FIELD_ID_CONTACT,
                    "values": [{"value": entity.utm_source}],
                },
                {
                    "field_id": UTM_MEDIUM_FIELD_ID_CONTACT,
                    "values": [{"value": entity.utm_medium}],
                },
                {
                    "field_id": UTM_CAMPAIGN_FIELD_ID_CONTACT,
                    "values": [{"value": entity.utm_campaign}],
                },
                {
                    "field_id": UTM_CONTENT_FIELD_ID_CONTACT,
                    "values": [{"value": entity.utm_content}],
                },
            ],
        }
    ]

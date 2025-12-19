from typing import Any

from sqlalchemy import JSON, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}
    metadata = MetaData()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

"""
Utils for work with SQLAlchemy orm
"""
from typing import Optional
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute, \
    ColumnProperty, RelationshipProperty, aliased
from sqlalchemy.orm.util import AliasedClass


def get_related_mapper(
    mapper: DeclarativeMeta,
    field_name: str,
) -> Optional[DeclarativeMeta]:
    """
    returns declarative orm model from relationship field
    """
    mapper_field: InstrumentedAttribute = getattr(mapper, field_name, None)
    if mapper_field is None:
        return

    return mapper_field.property.mapper.class_


def get_column(
    mapper: DeclarativeMeta,
    field_name: str,
) -> Optional[InstrumentedAttribute]:
    return getattr(mapper, field_name, None)


def is_column(
    mapper_field: InstrumentedAttribute
) -> bool:
    return isinstance(mapper_field.property, ColumnProperty)


def is_relationship(
    mapper_field: InstrumentedAttribute
) -> bool:
    return isinstance(mapper_field.property, RelationshipProperty)


def make_aliased_mapper(
    mapper: DeclarativeMeta,
    field_name: str,
) -> Optional[AliasedClass]:
    related_mapper = get_related_mapper(
        mapper=mapper,
        field_name=field_name
    )
    aliased_mapper = aliased(related_mapper, name=field_name)
    return aliased_mapper

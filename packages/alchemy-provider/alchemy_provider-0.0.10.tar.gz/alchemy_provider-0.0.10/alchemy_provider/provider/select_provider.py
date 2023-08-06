from __future__ import annotations
from abc import abstractmethod
from uuid import uuid4, UUID
from typing import Union, Type, List, Optional
from sqlalchemy import select
from sqlalchemy.sql import Select, Insert, Update
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty, \
    RelationshipProperty, InstrumentedAttribute, aliased
from sqlalchemy.orm.util import AliasedClass
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery, FIELD_NAME_SEPARATOR
from ..utils import AliasedManager
from .base import BaseProvider
from .join_provider import JoinProvider
from .pagination_provider import PaginationProvider
from .sorting_provider import SortingProvider


class SelectProvider(
    JoinProvider,
    PaginationProvider,
    SortingProvider,
    BaseProvider
):
    @abstractmethod
    async def select(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_select_stmt(self, *args, **kwargs):
        pass

    def _make_select_stmt(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        uuid: UUID = None,
    ) -> Select:
        uuid = uuid or uuid4()
        select_stmt = self._make_simple_select_stmt(
            query=query,
            mapper=mapper,
            uuid=uuid,
        )

        select_stmt = self.bind_pagination(
            query=query,
            select_stmt=select_stmt
        )

        select_stmt = self.bind_sorting(
            query=query,
            mapper=mapper,
            select_stmt=select_stmt,
        )

        if query.is_instance():
            select_stmt = self._bind_clause(
                clause=query.get_filters(),
                mapper=mapper,
                stmt=select_stmt,
                clause_binder=clause_binder,
                uuid=uuid,
            )

        AliasedManager.delete(uuid=uuid)

        return select_stmt

    def _make_select_from_stmt(
        self,
        query: CRUDQuery,
        stmt: Union[Insert, Update],
        mapper: DeclarativeMeta,
        uuid: Optional[UUID] = None,
    ) -> Select:
        uuid = uuid or uuid4()

        selectable_columns = self._get_selectable_columns(
            mapper=mapper,
        )
        returning_cte_alias = stmt.returning(*selectable_columns).cte().alias()
        aliased_mapper = aliased(mapper, alias=returning_cte_alias)

        select_stmt = self._make_simple_select_stmt(
            query=query.get_class(),
            mapper=aliased_mapper,
            uuid=uuid
        )

        AliasedManager.delete(uuid=uuid)

        return select_stmt

    def _make_select_from_insert(
        self,
        query: CRUDQuery,
        insert_stmt: Insert,
        mapper: DeclarativeMeta,
    ) -> Select:
        """
        with inserted_cte as (
            insert into test(id, name) values
            (1, 'some_name')
            returning id
        )
        select test.*, test2.*
        from test
        join inserted_cte on test.id = inserted_cte.id
        join test2 on test.test2_id = test2.id
        """
        return self._make_select_from_stmt(
            query=query,
            stmt=insert_stmt,
            mapper=mapper,
        )

    def _make_select_from_update(
        self,
        query: CRUDQuery,
        update_stmt: Update,
        mapper: DeclarativeMeta,
        uuid: UUID,
    ) -> Select:
        """
        with updated_cte as (
            update test
            set name = 'some_new_name'
            where id >= 1
            returning id
        )
        select test.*, test2.*
        from test
        join updated_cte on test.id = updated_cte.id
        join test2 on test.test2_id = test2.id
        """
        return self._make_select_from_stmt(
            query=query,
            stmt=update_stmt,
            mapper=mapper,
            uuid=uuid,
        )

    def _make_simple_select_stmt(
        self,
        query: Type[CRUDQuery],
        mapper: Union[DeclarativeMeta, AliasedClass],
        uuid: UUID,
        label_prefix: Optional[str] = None,
        select_stmt: Optional[Select] = None,
    ) -> Select:

        if select_stmt is None:
            select_stmt = select()

        type_hints = query.get_type_hints()

        for field_name, type_hint in type_hints.items():
            mapper_field = getattr(mapper, field_name, None)
            if mapper_field is None:
                continue

            if isinstance(mapper_field.property, ColumnProperty):
                select_stmt = select_stmt.add_columns(
                    mapper_field.label(
                        self._make_column_label(
                            mapper_field=mapper_field,
                            label_prefix=label_prefix
                        )
                    )
                )
                continue

            if isinstance(mapper_field.property, RelationshipProperty):
                aliased_mapper = AliasedManager.get_or_create(
                    uuid=uuid,
                    mapper=mapper,
                    field_name=field_name
                )

                select_stmt = self._join(
                    field_name=field_name,
                    query=query,
                    stmt=select_stmt,
                    mapper=mapper,
                    aliased_mapper=aliased_mapper,
                )

                select_stmt = self._make_simple_select_stmt(
                    select_stmt=select_stmt,
                    query=query.get_field_query(field_name),
                    uuid=uuid,
                    mapper=aliased_mapper,
                    label_prefix=field_name,
                )

        return select_stmt

    @staticmethod
    def _get_selectable_columns(
        mapper: DeclarativeMeta
    ) -> List[InstrumentedAttribute]:
        columns = list()
        for column_name, column in mapper.__dict__.items():
            if not isinstance(column, InstrumentedAttribute):
                continue

            if not isinstance(column.property, ColumnProperty):
                continue

            columns.append(column)

        return columns

    @staticmethod
    def _make_column_label(
        mapper_field: InstrumentedAttribute,
        label_prefix: Optional[str] = None,
    ) -> str:
        if label_prefix is None:
            return mapper_field.name

        return label_prefix + FIELD_NAME_SEPARATOR + mapper_field.name

    async def _select(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> List[CRUDQuery]:
        select_stmt = self._make_select_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder
        )

        scalar_result = await self._session.execute(select_stmt)

        return query.from_selected_rows(rows=scalar_result.all())

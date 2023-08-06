import typing

import sqlalchemy.orm

SingleExecuteParams = typing.Mapping[str, typing.Any]
MultiExecuteParams = typing.Sequence[SingleExecuteParams]
AnyExecuteParams = typing.Union[MultiExecuteParams, SingleExecuteParams]

COLUMNS_CLAUSE_ARGUMENT = typing.TypeVar(
    "COLUMNS_CLAUSE_ARGUMENT",
    bound=sqlalchemy.sql._typing._ColumnsClauseArgument[typing.Any],
)


class SessionMakerMixin:
    @classmethod
    def session_maker(cls) -> sqlalchemy.orm.sessionmaker:
        raise NotImplementedError(
            """
Inherit from Base first,
and implement @classmethod session_maker() in the DeclarativeBase of your models:

class Base(sa.orm.DeclarativeBase):
    @classmethod
    def session_maker(cls) -> sqlalchemy.orm.sessionmaker:
        return <namespace>.session_maker

class User(Base, dal_poc.DML): ...
            """
        )


class Insert(SessionMakerMixin):
    @classmethod
    def _insert_no_returning(cls, values: AnyExecuteParams) -> None:
        stmt = sqlalchemy.insert(cls)
        with cls.session_maker().begin() as session:
            session.execute(stmt, values)

    @classmethod
    def _insert_returning_result(
        cls,
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.insert(cls).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.execute(stmt, values)
        return result

    @classmethod
    def _insert_returning_scalar(
        cls,
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.insert(cls).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.scalars(stmt, values)
        return result

    @classmethod
    def insert(
        cls,
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> typing.Union[
        sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT],
        sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT],
        None,
    ]:
        match returning:
            case [one, two, *more]:
                return cls._insert_returning_result(values, [one, two, *more])
            case [one, *more]:
                return cls._insert_returning_scalar(values, [one, *more])
            case _:
                return cls._insert_no_returning(values)


class Update(SessionMakerMixin):
    @classmethod
    def _update_no_returning(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        values: AnyExecuteParams,
    ) -> None:
        stmt = sqlalchemy.update(cls).where(*where)
        with cls.session_maker().begin() as session:
            session.execute(
                stmt,
                values,
            )

    @classmethod
    def _update_returning_scalar(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT],
    ) -> sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.update(cls).where(*where).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.scalars(
                stmt,
                values,
            )
        return result

    @classmethod
    def _update_returning_result(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT],
    ) -> sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.update(cls).where(*where).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.execute(
                stmt,
                values,
            )
        return result

    @classmethod
    def update(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        values: AnyExecuteParams,
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> typing.Union[
        sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT],
        sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT],
        None,
    ]:
        match returning:
            case [one, two, *more]:
                return cls._update_returning_result(where, values, [one, two, *more])
            case [
                one,
            ]:
                return cls._update_returning_scalar(
                    where,
                    values,
                    [
                        one,
                    ],
                )
            case _:
                return cls._update_no_returning(where, values)


class Delete(SessionMakerMixin):
    @classmethod
    def _delete_no_returning(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
    ) -> None:
        stmt = sqlalchemy.delete(cls).where(*where)
        with cls.session_maker().begin() as session:
            session.execute(stmt)

    @classmethod
    def _delete_returning_scalar(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.delete(cls).where(*where).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.scalars(stmt)
        return result

    @classmethod
    def _delete_returning_result(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT]:
        stmt = sqlalchemy.delete(cls).where(*where).returning(*returning)
        with cls.session_maker().begin() as session:
            result = session.execute(stmt)
        return result

    @classmethod
    def delete(
        cls,
        where: typing.Sequence[sqlalchemy.ColumnExpressionArgument[bool]],
        returning: typing.Sequence[COLUMNS_CLAUSE_ARGUMENT] = (),
    ) -> typing.Union[
        sqlalchemy.ScalarResult[COLUMNS_CLAUSE_ARGUMENT],
        sqlalchemy.Result[COLUMNS_CLAUSE_ARGUMENT],
        None,
    ]:
        """
        :param where: filters affected row, send empty sequence to affect all rows explicitly
        :param returning: select returned columns, leave empty or send empty sequence for no return
            values, if only one value is provided, result will be scalar
        """
        match returning:
            case [one, two, *more]:
                return cls._delete_returning_result(where, [one, two, *more])
            case [one, *more]:
                return cls._delete_returning_scalar(where, [one, *more])
            case _:
                return cls._delete_no_returning(where)


class DML(Insert, Update, Delete):
    """helper class that package all dml method implementations insert, update and delete"""

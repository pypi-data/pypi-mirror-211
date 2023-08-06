import contextlib
import pathlib
import sqlite3

import pydantic
import pytest
import sqlalchemy.orm
from fake_session_maker import fsm

import model_dml


class Settings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    sqlalchemy_test_url: str
    sqlalchemy_test_file_name: str


settings = Settings()


def pytest_sessionstart():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    db = pathlib.Path(settings.sqlalchemy_test_file_name)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        con.commit()


def pytest_sessionfinish():
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    db = pathlib.Path(settings.sqlalchemy_test_file_name)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE users")
        con.commit()
    with contextlib.suppress(PermissionError):
        pathlib.Path(settings.sqlalchemy_test_file_name).unlink()


class Namespace:
    session_maker: sqlalchemy.orm.sessionmaker = None


class Base(sqlalchemy.orm.DeclarativeBase):
    @classmethod
    def session_maker(cls) -> sqlalchemy.orm.sessionmaker:
        return Namespace.session_maker


@pytest.fixture
def base():
    return Base


@pytest.fixture
def user(base):
    class User(base, model_dml.DML):
        __tablename__ = "users"
        __table_args__ = {"extend_existing": True}
        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
        name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30))

    return User


@pytest.fixture
def fake_session_maker() -> sqlalchemy.orm.sessionmaker:
    with fsm(
        db_url=settings.sqlalchemy_test_url,
        namespace=Namespace,
        symbol_name="session_maker",
        create_engine_kwargs={"echo": True},
    ) as fake_session_maker_:
        # the fake_session_maker won't auto-commit after transaction
        # and rollback after transaction
        yield fake_session_maker_

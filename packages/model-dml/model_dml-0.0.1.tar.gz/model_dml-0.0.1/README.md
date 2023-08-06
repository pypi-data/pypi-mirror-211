<p align="center">
    <a href="https://pypi.org/project/model_dml" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/model_dml.svg?color=%2334D058" alt="Supported Python versions">
    </a>
    <a href="https://pycqa.github.io/isort/" target="_blank">
        <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="Imports: isort">
    </a>
    <a href="https://pypi.org/project/model_dml" target="_blank">
        <img src="https://img.shields.io/pypi/dm/model_dml" alt="PyPI - Downloads">
    </a>
</p>

# model_dml

A package for SQLAlchemy models DML mixins.

## Features

- Three methods for DML operations: `insert`, `update`, `delete`.
- Add those methods to models through mixin classes.
- Support returning selected columns for all methods.

## Installation

```bash
pip install model_dml
```

## Usage

### Custom Base

To use `model_dml`, you need to create a custom base class for your models with a `session_maker`
method.

What is a sessionmaker:
- [Using a sessionmaker][Using a sessionmaker]
- [sessionmaker documentation and example][sessionmaker documentation and example]

```python
class Base(sqlalchemy.orm.DeclarativeBase):
    @classmethod
    def session_maker(cls) -> sqlalchemy.orm.sessionmaker:
        return <Namespace>.Session
```

This method exist to allow DML methods to access the `sessionmaker` without creating a new reference
that would also need to be monkey patched. By returning the `sessionmaker` from the namespace, only
`<Namespace>.Session` needs to be monkey patched.

### Compose your model with what you need

```python
class User(base, model_dml.Insert, model_dml.Update, model_dml.Delete):
    __tablename__ = "users"
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30))
```

You can use `model_dml.DML` which is a helper class that composes all the mixins together.

```python
class User(base, model_dml.DML):
    __tablename__ = "users"
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30))
```

### Use the DML methods

```python
user = User.insert(dict(name="John"))
user = User.insert({'name': "Jane"})
user = User.insert({'name': "Jack"}, returning=[User.id, User.name])
```

[Using a sessionmaker]: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
[sessionmaker documentation and example]: https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker
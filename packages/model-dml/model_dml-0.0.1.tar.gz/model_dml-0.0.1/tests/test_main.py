import sqlalchemy


def test_insert(fake_session_maker, user):
    user.insert({"name": "John"})
    with fake_session_maker() as session:
        check = session.get(user, 1)
        assert check.id == 1
        assert check.name == "John"


def test_insert_no_returning(fake_session_maker, user):
    result = user.insert({"name": "John"}, returning=[])
    assert result is None

    with fake_session_maker() as session:
        check = session.get(user, 1)
        assert check.id == 1
        assert check.name == "John"


def test_insert_entity(fake_session_maker, user):
    result = user.insert({"name": "John"}, returning=[user])
    first_row = next(result)

    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert first_row.id == check.id == 1
    assert first_row.name == check.name == "John"


def test_insert_scalar(fake_session_maker, user):
    result = user.insert({"name": "John"}, returning=[user.name])
    name = next(result)

    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert check.id == 1
    assert name == check.name == "John"


def test_insert_result(fake_session_maker, user):
    result = user.insert({"name": "John"}, returning=[user.id, user.name])
    first_row = next(result)

    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert first_row.id == check.id == 1
    assert first_row.name == check.name == "John"


def test_update(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    user.update([user.id == 1], {"name": "Jane"})
    with fake_session_maker() as session:
        check = session.get(user, 1)
        assert check.id == 1
        assert check.name == "Jane"


def test_update_no_returning(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    user.update([user.id == 1], {"name": "Jane"}, returning=())
    with fake_session_maker() as session:
        check = session.get(user, 1)
        assert check.id == 1
        assert check.name == "Jane"


def test_update_returning_tuples(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    result = user.update([user.id == 1], {"name": "Jane"}, returning=(user.id, user.name))
    first_row = next(result)
    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert first_row.id == check.id == 1
    assert first_row.name == check.name == "Jane"
    assert first_row == (1, "Jane")


def test_update_returning_entity(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    result = user.update([user.id == 1], {"name": "Jane"}, returning=(user,))
    first_row = next(result)
    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert first_row.id == check.id == 1
    assert first_row.name == check.name == "Jane"


def test_delete(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    result = user.delete([])
    assert result is None

    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert check is None


def test_delete_returning_result(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    result = user.delete([], returning=[user.id, user.name])
    first_row = next(result)
    assert first_row.id == 1
    assert first_row.name == "John"

    with fake_session_maker() as session:
        check = session.get(user, 1)
    assert check is None


def test_delete_returning_scalar(fake_session_maker, user):
    with fake_session_maker() as session:
        session.add(user(name="John"))
    result = user.delete([user.id == 1], returning=[user])
    first_row = next(result)
    assert first_row.id == 1
    assert first_row.name == "John"

    with fake_session_maker() as session:
        check = session.execute(
            sqlalchemy.text(
                """
        SELECT users.id AS users_id, users.name AS users_name
        FROM users
        WHERE users.id = 1
        """
            )
        ).first()

    assert check is None

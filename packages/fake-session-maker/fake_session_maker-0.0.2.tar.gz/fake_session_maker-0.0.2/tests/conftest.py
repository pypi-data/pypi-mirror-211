import pathlib
import sqlite3

import pytest
import sqlalchemy.orm

from fake_session_maker import fsm


@pytest.fixture(autouse=True, scope="session")
def db_migrate():
    db = pathlib.Path("./tests/test.sqlite")
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        con.commit()
    yield
    with sqlite3.connect(db) as con:
        cur.execute("DROP TABLE users")
        con.commit()
    db.unlink()


@pytest.fixture
def namespace():
    class Namespace:
        engine = sqlalchemy.create_engine(
            "sqlite:///tests/test.db",
            echo=True,
        )
        session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

    return Namespace


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


@pytest.fixture(scope="session")
def user_model():
    class User(Base):
        __tablename__ = "users"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String)

    return User


@pytest.fixture
def create_user(namespace, user_model):
    def create_user_(name: str):
        with namespace.session_maker.begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest.fixture
def fake_session_maker(namespace) -> sqlalchemy.orm.sessionmaker:
    with fsm(
        db_url="sqlite:///tests/test.sqlite",
        namespace=namespace,
        symbol_name="session_maker",
    ) as fake_session_maker_:
        # the fake_session_maker won't auto-commit after transaction
        # and rollback after transaction
        yield fake_session_maker_

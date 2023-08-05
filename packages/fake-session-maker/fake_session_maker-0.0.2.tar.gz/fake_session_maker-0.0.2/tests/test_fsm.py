import pytest


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_isolation(create_user, user_model, fake_session_maker, name):
    """
    this test is run twice thanks to the parametrize decorator, while the expected result
    from the database is that there is only one user with id=1
    """
    result = create_user(name)
    assert result == "success"
    with fake_session_maker() as session:
        assert session.query(user_model.id, user_model.name).all() == [(1, name)]

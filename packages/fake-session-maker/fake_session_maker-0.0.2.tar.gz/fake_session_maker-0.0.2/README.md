<p align="center">
    <a href="https://pypi.org/project/fake_session_maker" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/fake_session_maker.svg?color=%2334D058" alt="Supported Python versions">
    </a>
    <a href="https://pycqa.github.io/isort/" target="_blank">
        <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="Imports: isort">
    </a>
    <a href="https://pypi.org/project/fake_session_maker" target="_blank">
        <img src="https://img.shields.io/pypi/dm/fake_session_maker" alt="PyPI - Downloads">
    </a>
</p>

# fake_session_maker

The `fake_session_maker` is a SQLAlchemy and Pytest-based package designed to facilitate database
testing by replacing a classic SQLAlchemy `SessionMaker` context manager.

## Features

- Replaces the SQLAlchemy `SessionMaker` context manager with a "read-only" session during tests.
- Rollbacks database state at the end of each test, ensuring isolation between tests.
- Simple fixture-based usage integrates smoothly with your Pytest suite.

## Drawbacks

Code that plan to be tested using `fake_session_maker` have the following limitations:

- Prevent the use of `SessionMaker.rollback()` by hands as every previous "prod-only" commit will be
  rolled back too
- Cannot rely on results after a forced `SessionMaker.rollback()` if a `SessionMaker.flush()` fails
  for the same reason as above

### Mitigation

- For such tests, a snapshot of the database can be taken before the test and restored after the
  test using a fixture. This is not provided by `fake_session_maker` but can be implemented by the
  user. This is more expensive than using `fake_session_maker` but won't suffer from the drawbacks

## Prerequisites

To use `fake_session_maker`, you'll need:

- Python (>=3.7)
- SQLAlchemy (>=1.4 <3.0)
- Pytest (>=6.2.2)

## Usage

### Define the fixture

Below is an example of how to use fake_session_maker in a pytest fixture:

```python
import pytest
from fake_session_maker import fsm


# Assuming Namespace is where the session_maker is defined

@pytest.fixture
def fake_session_maker():
    with fsm(
            db_url="sqlite:///tests/test.sqlite",
            namespace=Namespace,
            symbol_name="session_maker",
    ) as fake_session_maker_:
        yield fake_session_maker_

# Now, you can use fake_session_maker in your tests
```

### Use the fixture

Below is an example of how to use fake_session_maker fixture in a test:

```python
# Each test will have a fresh database, empty of any data
@pytest.mark.parametrize("name", ["jane", "joe"])
def test_create_example(fake_session_maker, name):
    result = create_example('test')
    assert result == 'success'
    with fake_session_maker() as session:
        # Each time we check, only the data created in this test will be present
        assert session.query(models.User).count() == 1
```

See the [tests.test_fsm.py](tests/test_fsm.py) directory for a full example.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Testing

If you want to run the tests locally, you can follow instructions here:
[CONTRIBUTING.md #testing](CONTRIBUTING.md#testing).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
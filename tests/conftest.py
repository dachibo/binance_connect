import pytest
import json


@pytest.fixture(scope="session")
def history_klines():
    with open("tests/history_klines.json", "r") as fp:
        data = json.load(fp)
        yield data

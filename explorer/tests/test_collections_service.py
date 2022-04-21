from unittest import mock

import petl as etl
import pytest

from explorer.services import collections

pytestmark = pytest.mark.django_db


@pytest.fixture
def people_table():
    return etl.fromdicts([{"name": "Obi Wan"}, {"name": "Anakin"}])


@mock.patch("explorer.services.collections.prepare_people_collection_table")
def test_fetching_and_saving(mock_prepare_table, people_table):
    mock_prepare_table.return_value = people_table

    collection = collections.fetch_and_save_new_collection()
    assert collection.id is not None
    assert collection.file is not None
    # NOTE: check if it is CSV-like format
    assert collection.file.read() == b"name\r\nObi Wan\r\nAnakin\r\n"

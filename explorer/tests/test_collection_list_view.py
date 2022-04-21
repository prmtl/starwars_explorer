import pytest
from django.core.files.base import ContentFile

from explorer.models import Collection

pytestmark = pytest.mark.django_db


@pytest.fixture
def collection():
    c = Collection()
    c.file = ContentFile(b"field\n\rvalue\n\r", "file.csv")
    c.save()
    return c


def test_no_collection(client):
    response = client.get("/")
    assert len(response.context["object_list"]) == 0
    assert "No data yet." in response.content.decode()


def test_at_least_one_collection(client, collection):
    response = client.get("/")
    assert len(response.context["object_list"]) == 1
    assert str(collection.id) in response.content.decode()

from typing import Optional

from django.db import transaction

from explorer.models import Collection
from explorer.services import processing, swapi


def prepare_people_collection_table():
    # NOTE: fetching both full datasets will save us requests numbers in comparison to
    # for example fetching people and then fetch each planet with one requets
    # but if there would be much more data not fitting into memory this would need to be load into some
    # datastore (DB) from which we could then fetch it
    people_raw_data = swapi.fetch_swapi_people_dataset()
    planets_raw_data = swapi.fetch_swapi_planets_dataset()

    return processing.process_people_and_planets_data(people=people_raw_data, planets=planets_raw_data)


def get_filename_for_collection(collection: Collection):
    return f"{collection.id}.csv"


@transaction.atomic
def fetch_and_save_new_collection():
    """Downloads fresh data from SWAPI, process data and save it as a new Collection entry"""
    people = prepare_people_collection_table()
    file = processing.as_csv_contentfile(people)

    collection = Collection.objects.create()
    filename = get_filename_for_collection(collection)
    collection.file.save(filename, file)

    return collection


def load_collection_data(collection: Collection, limit: Optional[int] = None):
    return processing.load_table_as_dicts(filepath=collection.file.path, limit=limit)


def load_table(collection):
    return processing.load_table(filepath=collection.file.path)

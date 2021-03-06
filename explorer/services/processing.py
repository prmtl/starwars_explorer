from typing import List, Optional

import petl as etl
from django.core.files.base import ContentFile
from django.utils.dateparse import parse_datetime

# NOTE: I wanted to name this service 'etl' but this is used often in petl examples so to avoid confusion
# it is 'processing'

SHORT_DATE_FORMAT = "%Y-%m-%d"
PEOPLE_HEADERS = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "edited",
]
PLANETS_HEADERS = ["name", "url"]


def reformat_date(date_string: str, date_format: str = SHORT_DATE_FORMAT):
    date = parse_datetime(date_string)
    return date.strftime(date_format)


def process_people_and_planets_data(people, planets):
    """Merges people with planets and applies various operations on merged table fields."""
    people_table = etl.fromdicts(people, header=PEOPLE_HEADERS)
    planets_table = etl.fromdicts(planets, header=PLANETS_HEADERS)

    # NOTE: I am not sure if join is actually better (time, resources) than
    # just doing a convert on a homeworld which will fetch data from a dict of planets
    # It might be the case that this is "shooting a fly with a cannon"
    return (
        people_table.join(planets_table, lkey="homeworld", rkey="url", rprefix="planet_")
        .cutout("homeworld")
        .rename({"edited": "date", "planet_name": "homeworld"})
        .convert("date", reformat_date)
    )


def as_csv_contentfile(table):
    source = etl.MemorySource()
    table.tocsv(source)
    return ContentFile(source.getvalue())


def load_table_as_dicts(filepath: str, limit: Optional[int] = None):
    return etl.fromcsv(filepath).rowslice(limit).dicts()


def load_table(filepath: str):
    return etl.fromcsv(filepath)


def count_selected_fields_combinations_for_table(table, selected_fields: List[str]):
    """Return counts of field combinations in form of a dict list

    ```
    [
        {"filedA": "x",  "fieldB": "y", "value": 2},
        {"filedA": "r",  "fieldB": "y", "value": 1},
        ...
    ]
    ```
    """
    if not selected_fields:
        raise ValueError("At least one field need to be slected")
    return table.aggregate(key=selected_fields, aggregation=len).dicts()

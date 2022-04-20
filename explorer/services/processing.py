from typing import Any, Dict

import petl as etl
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


def process_people_and_planets_data(people: Dict[str, Any], planets: Dict[str, Any]):
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

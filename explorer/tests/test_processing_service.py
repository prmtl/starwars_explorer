import pytest

from explorer.services.processing import process_people_and_planets_data, reformat_date

PEOPLE = [
    {
        "name": "Qui-Gon Jinn",
        "height": "193",
        "mass": "89",
        "hair_color": "brown",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "92BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": ["https://swapi.dev/api/films/4/"],
        "species": [],
        "vehicles": ["https://swapi.dev/api/vehicles/38/"],
        "starships": [],
        "created": "2014-12-19T16:54:53.618000Z",
        "edited": "2014-12-20T21:17:50.375000Z",
        "url": "https://swapi.dev/api/people/32/",
    },
    {
        "name": "Nute Gunray",
        "height": "191",
        "mass": "90",
        "hair_color": "none",
        "skin_color": "mottled green",
        "eye_color": "red",
        "birth_year": "unknown",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [
            "https://swapi.dev/api/films/4/",
            "https://swapi.dev/api/films/5/",
            "https://swapi.dev/api/films/6/",
        ],
        "species": ["https://swapi.dev/api/species/11/"],
        "vehicles": [],
        "starships": [],
        "created": "2014-12-19T17:05:57.357000Z",
        "edited": "2014-12-20T21:17:50.377000Z",
        "url": "https://swapi.dev/api/people/33/",
    },
    {
        "name": "Padmé Amidala",
        "height": "185",
        "mass": "45",
        "hair_color": "brown",
        "skin_color": "light",
        "eye_color": "brown",
        "birth_year": "46BBY",
        "gender": "female",
        "homeworld": "https://swapi.dev/api/planets/3/",
        "films": [
            "https://swapi.dev/api/films/4/",
            "https://swapi.dev/api/films/5/",
            "https://swapi.dev/api/films/6/",
        ],
        "species": [],
        "vehicles": [],
        "starships": [
            "https://swapi.dev/api/starships/39/",
            "https://swapi.dev/api/starships/49/",
            "https://swapi.dev/api/starships/64/",
        ],
        "created": "2014-12-19T17:28:26.926000Z",
        "edited": "2014-12-20T21:17:50.381000Z",
        "url": "https://swapi.dev/api/people/35/",
    },
    {
        "name": "Jar Jar Binks",
        "height": "196",
        "mass": "66",
        "hair_color": "none",
        "skin_color": "orange",
        "eye_color": "orange",
        "birth_year": "52BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": ["https://swapi.dev/api/films/4/", "https://swapi.dev/api/films/5/"],
        "species": ["https://swapi.dev/api/species/12/"],
        "vehicles": [],
        "starships": [],
        "created": "2014-12-19T17:29:32.489000Z",
        "edited": "2014-12-20T21:17:50.383000Z",
        "url": "https://swapi.dev/api/people/36/",
    },
]

PLANETS = [
    {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/2/",
            "https://swapi.dev/api/people/4/",
            "https://swapi.dev/api/people/6/",
            "https://swapi.dev/api/people/7/",
            "https://swapi.dev/api/people/8/",
            "https://swapi.dev/api/people/9/",
            "https://swapi.dev/api/people/11/",
            "https://swapi.dev/api/people/43/",
            "https://swapi.dev/api/people/62/",
        ],
        "films": [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/3/",
            "https://swapi.dev/api/films/4/",
            "https://swapi.dev/api/films/5/",
            "https://swapi.dev/api/films/6/",
        ],
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z",
        "url": "https://swapi.dev/api/planets/1/",
    },
    {
        "name": "Yavin IV",
        "rotation_period": "24",
        "orbital_period": "4818",
        "diameter": "10200",
        "climate": "temperate, tropical",
        "gravity": "1 standard",
        "terrain": "jungle, rainforests",
        "surface_water": "8",
        "population": "1000",
        "residents": [],
        "films": ["https://swapi.dev/api/films/1/"],
        "created": "2014-12-10T11:37:19.144000Z",
        "edited": "2014-12-20T20:58:18.421000Z",
        "url": "https://swapi.dev/api/planets/3/",
    },
]


@pytest.mark.parametrize(
    "date,expected",
    (
        (
            "2014-12-19T16:54:53.618000Z",
            "2014-12-19",
        ),
        ("2014-12-20", "2014-12-20"),
    ),
)
def test_refromatting_date(date, expected):
    assert reformat_date(date) == expected


# NOTE: this is dummy test to see if our processing pipleline actually works
def test_simple_data_processing():
    table = process_people_and_planets_data(PEOPLE, PLANETS)
    rows = list(table.dicts())
    assert len(rows) == len(PEOPLE)
    assert sorted(table.header()) == sorted(
        (
            "name",
            "height",
            "mass",
            "hair_color",
            "skin_color",
            "eye_color",
            "birth_year",
            "gender",
            "date",
            "homeworld",
        )
    )

    for row in rows:
        assert "https" not in row["homeworld"]

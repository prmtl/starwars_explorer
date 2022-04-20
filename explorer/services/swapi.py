import httpx


# NOTE: I just like use httpx and requests lib was not a strong requirement
# NOTE: I would also add detailed logging for recording fetching progress
# NOTE: this is non-async version, but with httpx AsyncClient it can easily be switched to such
# if we would want to but on devserver we will not see the gains
def _fetch_swapi_entity_dataset(entity_name: str):
    url = f"https://swapi.dev/api/{entity_name}/"
    while True:
        response = httpx.get(url)
        entities_data = response.json()
        for entity in entities_data.get("results"):
            yield entity
        if next := entities_data.get("next"):
            url = next
        else:
            break


def fetch_swapi_people_dataset():
    yield from _fetch_swapi_entity_dataset("people")


def fetch_swapi_planets_dataset():
    yield from _fetch_swapi_entity_dataset("planets")

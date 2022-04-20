# starwars_explorer

## Setting up a project

Project requires recent version od `Docker` installed on a machine.

To build and run the app:

```
docker compose up -d
```

Alternatively it can be run without `Docker` but then some `env` variables need to be set.
Most important would be `DATABASE_URL` to point it to some SQL database, but it was only tested
with PostgreSQL (but it is simple enough that there should be no problem with any kind, including SQLite)


## Running tests

```
docker compose exec app py.test -vv
```


## See logs


```
docker compose logs app
```

## Possible improvements

 * Integrate Sentry for reporting errors (must-have for production)
 * Integrate tools like DataDog for gathering logs and metrics
 * Use structured logs (like `python-json-logger`)
 * Use external storage for files (object storage like S3, persitent volumes, maybe EBS)
 * Record log of downloading new dataset
 * Consider using some kind of a worker for moving as much as possible to background (Celery) if it would not fit into request time limit
 * Prevent users from starting multiple downloads at the same time
 * For testing views I would try to use tool like Cypress
 * Depending of the use case of the app it might be worth exposing API of some kind (REST, or GQL) and then use that API to implement fancy UI.
 * Add Makefile as a helper for running common commands
